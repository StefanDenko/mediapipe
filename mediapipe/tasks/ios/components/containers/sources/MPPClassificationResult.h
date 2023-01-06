// Copyright 2023 The MediaPipe Authors.
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
#import "mediapipe/tasks/ios/components/containers/sources/MPPCategory.h"

NS_ASSUME_NONNULL_BEGIN

/** Represents the list of classification for a given classifier head. Typically used as a result
 * for classification tasks.
 **/
NS_SWIFT_NAME(Classifications)
@interface MPPClassifications : NSObject

/**
 * The index of the classifier head these entries refer to. This is useful for multi-head models.
 **/
@property(nonatomic, readonly) NSInteger headIndex;

/** The optional name of the classifier head, which is the corresponding tensor metadata name. **/
@property(nonatomic, readonly, nullable) NSString *headName;

/** An array of `MPPCategory` objects containing the predicted categories. **/
@property(nonatomic, readonly) NSArray<MPPCategory *> *categories;

/**
 * Initializes a new `MPPClassifications` object with the given head index and array of categories.
 * Head name is initialized to `nil`.
 *
 * @param headIndex The index of the classifier head.
 * @param categories  An array of `MPPCategory` objects containing the predicted categories.
 *
 * @return An instance of `MPPClassifications` initialized with the given head index and
 * array of categories.
 **/
- (instancetype)initWithHeadIndex:(NSInteger)headIndex
                       categories:(NSArray<MPPCategory *> *)categories;

/**
 * Initializes a new `MPPClassifications` with the given head index, head name and array of
 * categories.
 *
 * @param headIndex The index of the classifier head.
 * @param headName The name of the classifier head, which is the corresponding tensor metadata
 * name.
 * @param categories An array of `MPPCategory` objects containing the predicted categories.
 *
 * @return An object of `MPPClassifications` initialized with the given head index, head name and
 * array of categories.
 **/
- (instancetype)initWithHeadIndex:(NSInteger)headIndex
                         headName:(nullable NSString *)headName
                       categories:(NSArray<MPPCategory *> *)categories NS_DESIGNATED_INITIALIZER;

- (instancetype)init NS_UNAVAILABLE;

+ (instancetype)new NS_UNAVAILABLE;                       

@end

/**
 * Represents the classification results of a model. Typically used as a result for classification
 * tasks.
 **/
NS_SWIFT_NAME(ClassificationResult)
@interface MPPClassificationResult : NSObject

/** An Array of `MPPClassifications` objects containing the predicted categories for each head of
 * the model. 
 **/
@property(nonatomic, readonly) NSArray<MPPClassifications *> *classifications;

/** The optional timestamp (in milliseconds) of the start of the chunk of data corresponding to
 * these results. If it is set to the value -1, it signifies the absence of a time stamp. This is
 * only used for classification on time series (e.g. audio classification). In these use cases, the
 * amount of data to process might exceed the maximum size that the model can process: to solve
 * this, the input data is split into multiple chunks starting at different timestamps.
 **/
@property(nonatomic, readonly) NSInteger timestampMs;

/**
 * Initializes a new `MPPClassificationResult` with the given array of classifications. This method
 * must be used when no time stamp needs to be specified. It sets the property `timestampMs` to -1.
 *
 * @param classifications An Aaray of `MPPClassifications` objects containing classifier
 * predictions per classifier head.
 *
 * @return An instance of MPPClassificationResult initialized with the given array of
 * classifications.
 **/
- (instancetype)initWithClassifications:(NSArray<MPPClassifications *> *)classifications;

/**
 * Initializes a new `MPPClassificationResult` with the given array of classifications and time
 * stamp (in milliseconds).
 *
 * @param classifications An Array of `MPPClassifications` objects containing the predicted
 * categories for each head of the model.
 * @param timeStampMs The timestamp (in milliseconds) of the start of the chunk of data
 * corresponding to these results.
 *
 * @return An instance of `MPPClassificationResult` initialized with the given array of
 * classifications and timestampMs.
 **/
- (instancetype)initWithClassifications:(NSArray<MPPClassifications *> *)classifications
                            timestampMs:(NSInteger)timestampMs;

@end

NS_ASSUME_NONNULL_END
