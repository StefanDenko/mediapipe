// Copyright 2022 The MediaPipe Authors.
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

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/**
 * MediaPipe Tasks delegate.
 */
 typedef NS_ENUM(NSUInteger, MPPDelegate) {
   /** CPU. */
   MPPDelegateCPU,

   /** GPU. */
   MPPDelegateGPU
 } NS_SWIFT_NAME(Delegate);

/**
 * Holds the base options that is used for creation of any type of task. It has fields with
 * important information acceleration configuration, TFLite model source etc.
 */
NS_SWIFT_NAME(BaseOptions)
@interface MPPBaseOptions : NSObject <NSCopying>

/**
 * The absolute path to a model asset file (a tflite model or a model asset bundle file) stored in the app bundle.
 */
@property(nonatomic, copy) NSString *modelAssetPath;

/**
 * Device delegate to run the MediaPipe pipeline. If the delegate is not set, the default
 * delegate CPU is used.
 */
@property(nonatomic) MPPDelegate delegate;

@end

NS_ASSUME_NONNULL_END
