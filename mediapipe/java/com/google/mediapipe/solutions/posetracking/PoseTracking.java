// Copyright 2021 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.google.mediapipe.solutions.posetracking;

import android.content.Context;
import android.util.Log;

import com.google.common.collect.ImmutableList;
import com.google.mediapipe.formats.proto.LandmarkProto;
import com.google.mediapipe.framework.MediaPipeException;
import com.google.mediapipe.framework.Packet;
import com.google.mediapipe.framework.PacketGetter;
import com.google.mediapipe.solutioncore.ErrorListener;
import com.google.mediapipe.solutioncore.ImageSolutionBase;
import com.google.mediapipe.solutioncore.OutputHandler;
import com.google.mediapipe.solutioncore.ResultListener;
import com.google.mediapipe.solutioncore.SolutionInfo;
import com.google.mediapipe.formats.proto.DetectionProto.Detection;
import com.google.protobuf.InvalidProtocolBufferException;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Nullable;

/**
 * MediaPipe Face Detection Solution API.
 *
 * <p>MediaPipe Face Detection processes a {@link TextureFrame} or a {@link Bitmap} and returns the
 * {@link PoseTrackingResult} representing each detected face. Please refer to
 * https://solutions.mediapipe.dev/face_detection#android-solution-api for usage examples.
 */
public class PoseTracking extends ImageSolutionBase {
  private static final String TAG = "PoseTracking";

  private static final String GRAPH_NAME = "pose_tracking_gpu_image.binarypb";
  private static final String IMAGE_INPUT_STREAM = "input_video";
  private static final ImmutableList<String> OUTPUT_STREAMS =
      ImmutableList.of("pose_detection", "throttled_input_video","output_video","pose_landmarks");
  private static final int DETECTIONS_INDEX = 0;
  private static final int INPUT_IMAGE_INDEX = 1;
  private static final int OUTPUT_IMAGE_INDEX = 2;
  private static final int LANDMARKS_INDEX = 3;
  private final OutputHandler<PoseTrackingResult> outputHandler;
  public PoseTrackingOptions options;
  /**
   * Initializes MediaPipe Face Detection solution.
   *
   * @param context an Android {@link Context}.
   * @param poseTrackingOptions the configuration options defined in {@link PoseTrackingOptions}.
   */
  public PoseTracking(Context context, PoseTrackingOptions poseTrackingOptions) {
    options = poseTrackingOptions;
    outputHandler = new OutputHandler<>();
    outputHandler.setOutputConverter(
        packets -> {
          PoseTrackingResult.Builder poseTrackingResultBuilder = PoseTrackingResult.builder();
          try {
            Packet packet = packets.get(DETECTIONS_INDEX);
            if (!packet.isEmpty()){
              try {
                byte[] bytes = PacketGetter.getProtoBytes(packet);
                Detection det = Detection.parseFrom(bytes);
                poseTrackingResultBuilder.setMultiPoseDetections(
                        ImmutableList.<Detection>of(det));

//                Detection det = PacketGetter.getProto(packet, Detection.getDefaultInstance());
                Log.v(TAG,"Packet not empty");

              }catch (InvalidProtocolBufferException e){
                Log.e(TAG,e.getMessage());
                poseTrackingResultBuilder.setMultiPoseDetections(
                        ImmutableList.<Detection>of());

              }

            }else {
              poseTrackingResultBuilder.setMultiPoseDetections(
                      getProtoVector(packets.get(DETECTIONS_INDEX), Detection.parser()));
            }

            Packet landmarksPacket = packets.get(LANDMARKS_INDEX);
            if (landmarksPacket.isEmpty()){
              poseTrackingResultBuilder.setMultiPoseLandmarks(ImmutableList.of());
            }else {
              byte[] landmarkBytes = PacketGetter.getProtoBytes(landmarksPacket);
              LandmarkProto.LandmarkList landmarks = LandmarkProto.LandmarkList.parseFrom(landmarkBytes);
//              List<LandmarkProto.Landmark> landmarks = getProtoVector(landmarksPacket, LandmarkProto.Landmark.parser());
              poseTrackingResultBuilder.setMultiPoseLandmarks(landmarks.getLandmarkList());
            }



          } catch (MediaPipeException e) {
            reportError("Error occurs while getting MediaPipe pose tracking results.", e);
          } catch (InvalidProtocolBufferException e) {
            e.printStackTrace();
          }

          int imageIndex = options.landmarkVisibility() ? OUTPUT_IMAGE_INDEX : INPUT_IMAGE_INDEX;
          return poseTrackingResultBuilder
              .setImagePacket(packets.get(imageIndex))
              .setTimestamp(
                  staticImageMode ? Long.MIN_VALUE : packets.get(imageIndex).getTimestamp())
              .build();
        });

    SolutionInfo solutionInfo =
        SolutionInfo.builder()
            .setBinaryGraphPath(
                    GRAPH_NAME)
            .setImageInputStreamName(IMAGE_INPUT_STREAM)
            .setOutputStreamNames(OUTPUT_STREAMS)
            .setStaticImageMode(options.staticImageMode())
            .build();

    initialize(context, solutionInfo, outputHandler);
    Map<String, Packet> inputSidePackets = new HashMap<>();
//    inputSidePackets.put("enable_segmentation", packetCreator.createBool(false));
    inputSidePackets.put("model_complexity",packetCreator.createInt32(options.modelComplexity()));
    inputSidePackets.put("smooth_landmarks",packetCreator.createBool(options.smoothLandmarks()));
    start(inputSidePackets);
  }

  /**
   * Sets a callback to be invoked when a {@link PoseTrackingResult} becomes available.
   *
   * @param listener the {@link ResultListener} callback.
   */
  public void setResultListener(ResultListener<PoseTrackingResult> listener) {
    this.outputHandler.setResultListener(listener);
  }

  /**
   * Sets a callback to be invoked when the Face Detection solution throws errors.
   *
   * @param listener the {@link ErrorListener} callback.
   */
  public void setErrorListener(@Nullable ErrorListener listener) {
    this.outputHandler.setErrorListener(listener);
    this.errorListener = listener;
  }
}
