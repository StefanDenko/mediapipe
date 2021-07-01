#ifndef FACE_MESH_LIBRARY_H
#define FACE_MESH_LIBRARY_H

#ifdef COMPILING_DLL
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT __declspec(dllimport)
#endif

#include <cstdlib>
#include <string>
#include <memory>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/calculator_graph.h"
#include "mediapipe/framework/formats/image_frame.h"
#include "mediapipe/framework/formats/image_frame_opencv.h"
#include "mediapipe/framework/formats/landmark.pb.h"
#include "mediapipe/framework/port/file_helpers.h"
#include "mediapipe/framework/port/opencv_highgui_inc.h"
#include "mediapipe/framework/port/opencv_imgproc_inc.h"
#include "mediapipe/framework/port/opencv_video_inc.h"
#include "mediapipe/framework/port/parse_text_proto.h"
#include "mediapipe/framework/port/status.h"

class FaceMeshDetector {
public:
  FaceMeshDetector();
  ~FaceMeshDetector() = default;
  std::vector<cv::Point2f> *ProcessFrame(cv::Mat &camera_frame);

private:
  absl::Status InitFaceMeshDetector();
  absl::Status ProcessFrameWithStatus(cv::Mat &camera_frame);

  static const char kInputStream[];
  static const char kOutputStream_landmarks[];
  static const char kOutputStream_faceCount[];

  static const std::string graphConfig;

  mediapipe::CalculatorGraph graph;
  
  std::unique_ptr<mediapipe::OutputStreamPoller> landmarks_poller_ptr;
  std::unique_ptr<mediapipe::OutputStreamPoller> face_count_poller_ptr;
};

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT FaceMeshDetector *FaceMeshDetector_Construct();

DLLEXPORT void FaceMeshDetector_Destruct(FaceMeshDetector *detector);

DLLEXPORT void *FaceMeshDetector_ProcessFrame(FaceMeshDetector *detector,
                                              cv::Mat &camera_frame);

#ifdef __cplusplus
};
#endif
#endif