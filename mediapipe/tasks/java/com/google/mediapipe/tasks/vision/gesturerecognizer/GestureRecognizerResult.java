// Copyright 2022 The MediaPipe Authors. All Rights Reserved.
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

package com.google.mediapipe.tasks.vision.gesturerecognizer;

import com.google.auto.value.AutoValue;
import com.google.mediapipe.formats.proto.LandmarkProto;
import com.google.mediapipe.formats.proto.ClassificationProto.Classification;
import com.google.mediapipe.formats.proto.ClassificationProto.ClassificationList;
import com.google.mediapipe.tasks.components.containers.Category;
import com.google.mediapipe.tasks.components.containers.Landmark;
import com.google.mediapipe.tasks.components.containers.NormalizedLandmark;
import com.google.mediapipe.tasks.core.TaskResult;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Represents the gesture recognition results generated by {@link GestureRecognizer}. */
@AutoValue
public abstract class GestureRecognizerResult implements TaskResult {

  private static final int kGestureDefaultIndex = -1;

  /**
   * Creates a {@link GestureRecognizerResult} instance from the lists of landmarks, handedness, and
   * gestures protobuf messages.
   *
   * @param landmarksProto a List of {@link NormalizedLandmarkList}
   * @param worldLandmarksProto a List of {@link LandmarkList}
   * @param handednessesProto a List of {@link ClassificationList}
   * @param gesturesProto a List of {@link ClassificationList}
   */
  static GestureRecognizerResult create(
      List<LandmarkProto.NormalizedLandmarkList> landmarksProto,
      List<LandmarkProto.LandmarkList> worldLandmarksProto,
      List<ClassificationList> handednessesProto,
      List<ClassificationList> gesturesProto,
      long timestampMs) {
    List<List<NormalizedLandmark>> multiHandLandmarks = new ArrayList<>();
    List<List<Landmark>> multiHandWorldLandmarks = new ArrayList<>();
    List<List<Category>> multiHandHandednesses = new ArrayList<>();
    List<List<Category>> multiHandGestures = new ArrayList<>();
    for (LandmarkProto.NormalizedLandmarkList handLandmarksProto : landmarksProto) {
      List<NormalizedLandmark> handLandmarks = new ArrayList<>();
      multiHandLandmarks.add(handLandmarks);
      for (LandmarkProto.NormalizedLandmark handLandmarkProto :
          handLandmarksProto.getLandmarkList()) {
        handLandmarks.add(
            com.google.mediapipe.tasks.components.containers.NormalizedLandmark.create(
                handLandmarkProto.getX(), handLandmarkProto.getY(), handLandmarkProto.getZ()));
      }
    }
    for (LandmarkProto.LandmarkList handWorldLandmarksProto : worldLandmarksProto) {
      List<com.google.mediapipe.tasks.components.containers.Landmark> handWorldLandmarks =
          new ArrayList<>();
      multiHandWorldLandmarks.add(handWorldLandmarks);
      for (LandmarkProto.Landmark handWorldLandmarkProto :
          handWorldLandmarksProto.getLandmarkList()) {
        handWorldLandmarks.add(
            com.google.mediapipe.tasks.components.containers.Landmark.create(
                handWorldLandmarkProto.getX(),
                handWorldLandmarkProto.getY(),
                handWorldLandmarkProto.getZ()));
      }
    }
    for (ClassificationList handednessProto : handednessesProto) {
      List<Category> handedness = new ArrayList<>();
      multiHandHandednesses.add(handedness);
      for (Classification classification : handednessProto.getClassificationList()) {
        handedness.add(
            Category.create(
                classification.getScore(),
                classification.getIndex(),
                classification.getLabel(),
                classification.getDisplayName()));
      }
    }
    for (ClassificationList gestureProto : gesturesProto) {
      List<Category> gestures = new ArrayList<>();
      multiHandGestures.add(gestures);
      for (Classification classification : gestureProto.getClassificationList()) {
        gestures.add(
            Category.create(
                classification.getScore(),
                // Gesture index is not used, because the final gesture result comes from multiple
                // classifiers.
                kGestureDefaultIndex,
                classification.getLabel(),
                classification.getDisplayName()));
      }
    }
    return new AutoValue_GestureRecognizerResult(
        timestampMs,
        Collections.unmodifiableList(multiHandLandmarks),
        Collections.unmodifiableList(multiHandWorldLandmarks),
        Collections.unmodifiableList(multiHandHandednesses),
        Collections.unmodifiableList(multiHandGestures));
  }

  @Override
  public abstract long timestampMs();

  /** Hand landmarks of detected hands. */
  public abstract List<List<NormalizedLandmark>> landmarks();

  /** Hand landmarks in world coordniates of detected hands. */
  public abstract List<List<Landmark>> worldLandmarks();

  /** Handedness of detected hands. */
  public abstract List<List<Category>> handednesses();

  /**
   * Recognized hand gestures of detected hands. Note that the index of the gesture is always -1,
   * because the raw indices from multiple gesture classifiers cannot consolidate to a meaningful
   * index.
   */
  public abstract List<List<Category>> gestures();
}
