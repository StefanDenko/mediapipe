# Copyright 2023 The MediaPipe Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for face stylizer."""

import enum
import os
from unittest import mock

import numpy as np
from absl.testing import absltest
from absl.testing import parameterized

from mediapipe.python._framework_bindings import image as image_module
from mediapipe.tasks.python.core import base_options as base_options_module
from mediapipe.tasks.python.components.containers import rect
from mediapipe.tasks.python.test import test_utils
from mediapipe.tasks.python.vision import face_stylizer
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode_module
from mediapipe.tasks.python.vision.core import image_processing_options as image_processing_options_module


_BaseOptions = base_options_module.BaseOptions
_Rect = rect.Rect
_Image = image_module.Image
_FaceStylizer = face_stylizer.FaceStylizer
_FaceStylizerOptions = face_stylizer.FaceStylizerOptions
_RUNNING_MODE = running_mode_module.VisionTaskRunningMode
_ImageProcessingOptions = image_processing_options_module.ImageProcessingOptions

_MODEL = 'face_stylizer.task'
_LARGE_FACE_IMAGE = "portrait.jpg"
_MODEL_IMAGE_SIZE = 256
_TEST_DATA_DIR = 'mediapipe/tasks/testdata/vision'


class ModelFileType(enum.Enum):
  FILE_CONTENT = 1
  FILE_NAME = 2


class FaceStylizerTest(parameterized.TestCase):

  def setUp(self):
    super().setUp()
    self.test_image = _Image.create_from_file(
        test_utils.get_test_data_path(
            os.path.join(_TEST_DATA_DIR, _LARGE_FACE_IMAGE)))
    self.model_path = test_utils.get_test_data_path(
        os.path.join(_TEST_DATA_DIR, _MODEL))

  def test_create_from_file_succeeds_with_valid_model_path(self):
    # Creates with default option and valid model file successfully.
    with _FaceStylizer.create_from_model_path(self.model_path) as stylizer:
      self.assertIsInstance(stylizer, _FaceStylizer)

  def test_create_from_options_succeeds_with_valid_model_path(self):
    # Creates with options containing model file successfully.
    base_options = _BaseOptions(model_asset_path=self.model_path)
    options = _FaceStylizerOptions(base_options=base_options)
    with _FaceStylizer.create_from_options(options) as stylizer:
      self.assertIsInstance(stylizer, _FaceStylizer)

  def test_create_from_options_fails_with_invalid_model_path(self):
    with self.assertRaisesRegex(
        RuntimeError, 'Unable to open file at /path/to/invalid/model.tflite'):
      base_options = _BaseOptions(
          model_asset_path='/path/to/invalid/model.tflite')
      options = _FaceStylizerOptions(base_options=base_options)
      _FaceStylizer.create_from_options(options)

  def test_create_from_options_succeeds_with_valid_model_content(self):
    # Creates with options containing model content successfully.
    with open(self.model_path, 'rb') as f:
      base_options = _BaseOptions(model_asset_buffer=f.read())
      options = _FaceStylizerOptions(base_options=base_options)
      stylizer = _FaceStylizer.create_from_options(options)
      self.assertIsInstance(stylizer, _FaceStylizer)

  @parameterized.parameters(
      (ModelFileType.FILE_NAME, _LARGE_FACE_IMAGE),
      (ModelFileType.FILE_CONTENT, _LARGE_FACE_IMAGE)
  )
  def test_stylize(self, model_file_type, image_file_name):
    # Load the test image.
    self.test_image = _Image.create_from_file(
      test_utils.get_test_data_path(
        os.path.join(_TEST_DATA_DIR, image_file_name)))
    # Creates stylizer.
    if model_file_type is ModelFileType.FILE_NAME:
      base_options = _BaseOptions(model_asset_path=self.model_path)
    elif model_file_type is ModelFileType.FILE_CONTENT:
      with open(self.model_path, 'rb') as f:
        model_content = f.read()
      base_options = _BaseOptions(model_asset_buffer=model_content)
    else:
      # Should never happen
      raise ValueError('model_file_type is invalid.')

    options = _FaceStylizerOptions(base_options=base_options)
    stylizer = _FaceStylizer.create_from_options(options)

    # Performs face stylization on the input.
    stylized_image = stylizer.stylize(self.test_image)
    self.assertIsInstance(stylized_image, _Image)
    # Closes the stylizer explicitly when the stylizer is not used in
    # a context.
    stylizer.close()

  @parameterized.parameters(
      (ModelFileType.FILE_NAME, _LARGE_FACE_IMAGE),
      (ModelFileType.FILE_CONTENT, _LARGE_FACE_IMAGE)
  )
  def test_stylize_in_context(self, model_file_type, image_file_name):
    # Load the test image.
    self.test_image = _Image.create_from_file(
      test_utils.get_test_data_path(
        os.path.join(_TEST_DATA_DIR, image_file_name)))
    # Creates stylizer.
    if model_file_type is ModelFileType.FILE_NAME:
      base_options = _BaseOptions(model_asset_path=self.model_path)
    elif model_file_type is ModelFileType.FILE_CONTENT:
      with open(self.model_path, 'rb') as f:
        model_content = f.read()
      base_options = _BaseOptions(model_asset_buffer=model_content)
    else:
      # Should never happen
      raise ValueError('model_file_type is invalid.')

    options = _FaceStylizerOptions(base_options=base_options)
    with _FaceStylizer.create_from_options(options) as stylizer:
      # Performs face stylization on the input.
      stylized_image = stylizer.stylize(self.test_image)
      self.assertIsInstance(stylized_image, _Image)
      self.assertEqual(stylized_image.width, _MODEL_IMAGE_SIZE)
      self.assertEqual(stylized_image.height, _MODEL_IMAGE_SIZE)

  def test_stylize_succeeds_with_region_of_interest(self):
    base_options = _BaseOptions(model_asset_path=self.model_path)
    options = _FaceStylizerOptions(base_options=base_options)
    with _FaceStylizer.create_from_options(options) as stylizer:
      # Load the test image.
      test_image = _Image.create_from_file(
        test_utils.get_test_data_path(
          os.path.join(_TEST_DATA_DIR, _LARGE_FACE_IMAGE)
        )
      )
      # Region-of-interest around the face.
      roi = _Rect(left=0.32, top=0.02, right=0.67, bottom=0.32)
      image_processing_options = _ImageProcessingOptions(roi)
      # Performs face stylization on the input.
      stylized_image = stylizer.stylize(test_image, image_processing_options)
      self.assertIsInstance(stylized_image, _Image)
      self.assertEqual(stylized_image.width, _MODEL_IMAGE_SIZE)
      self.assertEqual(stylized_image.height, _MODEL_IMAGE_SIZE)

  def test_stylize_succeeds_with_no_face_detected(self):
    base_options = _BaseOptions(model_asset_path=self.model_path)
    options = _FaceStylizerOptions(base_options=base_options)
    with _FaceStylizer.create_from_options(options) as stylizer:
      # Load the test image.
      test_image = _Image.create_from_file(
        test_utils.get_test_data_path(
          os.path.join(_TEST_DATA_DIR, _LARGE_FACE_IMAGE)
        )
      )
      # Region-of-interest that doesn't contain a human face.
      roi = _Rect(left=0.1, top=0.1, right=0.2, bottom=0.2)
      image_processing_options = _ImageProcessingOptions(roi)
      # Performs face stylization on the input.
      stylized_image = stylizer.stylize(test_image, image_processing_options)
      self.assertIsNone(stylized_image)

  def test_missing_result_callback(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.LIVE_STREAM,
    )
    with self.assertRaisesRegex(
        ValueError, r'result callback must be provided'
    ):
      with _FaceStylizer.create_from_options(options) as unused_stylizer:
        pass

  @parameterized.parameters((_RUNNING_MODE.IMAGE), (_RUNNING_MODE.VIDEO))
  def test_illegal_result_callback(self, running_mode):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=running_mode,
      result_callback=mock.MagicMock(),
    )
    with self.assertRaisesRegex(
        ValueError, r'result callback should not be provided'
    ):
      with _FaceStylizer.create_from_options(options) as unused_stylizer:
        pass

  def test_calling_stylize_for_video_in_image_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.IMAGE,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the video mode'
      ):
        stylizer.stylize_for_video(self.test_image, 0)

  def test_calling_stylize_async_in_image_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.IMAGE,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the live stream mode'
      ):
        stylizer.stylize_async(self.test_image, 0)

  def test_calling_classify_in_video_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.VIDEO,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the image mode'
      ):
        stylizer.stylize(self.test_image)

  def test_calling_classify_async_in_video_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.VIDEO,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the live stream mode'
      ):
        stylizer.stylize_async(self.test_image, 0)

  def test_classify_for_video_with_out_of_order_timestamp(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.VIDEO,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      unused_result = stylizer.stylize_for_video(self.test_image, 1)
      with self.assertRaisesRegex(
          ValueError, r'Input timestamp must be monotonically increasing'
      ):
        stylizer.stylize_for_video(self.test_image, 0)

  def test_stylize_for_video(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.VIDEO,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      for timestamp in range(0, 300, 30):
        stylized_image = stylizer.stylize_for_video(
          self.test_image, timestamp
        )
        self.assertIsInstance(stylized_image, _Image)
        self.assertEqual(stylized_image.width, _MODEL_IMAGE_SIZE)
        self.assertEqual(stylized_image.height, _MODEL_IMAGE_SIZE)

  def test_calling_stylize_in_live_stream_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.LIVE_STREAM,
      result_callback=mock.MagicMock(),
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the image mode'
      ):
        stylizer.stylize(self.test_image)

  def test_calling_stylize_for_video_in_live_stream_mode(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.LIVE_STREAM,
      result_callback=mock.MagicMock(),
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      with self.assertRaisesRegex(
          ValueError, r'not initialized with the video mode'
      ):
        stylizer.stylize_for_video(self.test_image, 0)

  def test_stylize_async_calls_with_illegal_timestamp(self):
    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.LIVE_STREAM,
      result_callback=mock.MagicMock(),
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      stylizer.stylize_async(self.test_image, 100)
      with self.assertRaisesRegex(
          ValueError, r'Input timestamp must be monotonically increasing'
      ):
        stylizer.stylize_async(self.test_image, 0)

  def test_stylize_async_calls(self):
    observed_timestamp_ms = -1

    def check_result(
        stylized_image: _Image, output_image: _Image, timestamp_ms: int
    ):
      self.assertIsInstance(stylized_image, _Image)
      self.assertEqual(stylized_image.width, _MODEL_IMAGE_SIZE)
      self.assertEqual(stylized_image.height, _MODEL_IMAGE_SIZE)
      self.assertTrue(
        np.array_equal(
          output_image.numpy_view(), self.test_image.numpy_view()
        )
      )
      self.assertLess(observed_timestamp_ms, timestamp_ms)
      self.observed_timestamp_ms = timestamp_ms

    options = _FaceStylizerOptions(
      base_options=_BaseOptions(model_asset_path=self.model_path),
      running_mode=_RUNNING_MODE.LIVE_STREAM,
      result_callback=check_result,
    )
    with _FaceStylizer.create_from_options(options) as stylizer:
      for timestamp in range(0, 300, 30):
        stylizer.stylize_async(self.test_image, timestamp)


if __name__ == '__main__':
  absltest.main()
