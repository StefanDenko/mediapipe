//
//  WANativeMTLCameraPreviewView.h
//  WebAR-iOS
//  基于Metal的相机预览视图，闪电拍照定制优化，具备相机预览的基础功能
//  Created by wangrenzhu on 2020/11/16.
//  Copyright © 2020 Taobao lnc. All rights reserved.
//

#import <MetalKit/MetalKit.h>
#import <AVFoundation/AVFoundation.h>
#import <QuarameraFramework/QuarameraCameraRender.h>
#import <QuarameraFramework/QuarameraMTLCameraRender.h>
#import <QuarameraFramework/QuarameraShareTexture.h>

@protocol QuarameraMTLCameraRenderViewDelegate

- (void)draw:(NSTimeInterval)frameTime;


/// 开放离屏相机纹理 用于外部分流
/// @param texture texture description
/// @param onScreenTexture 上屏纹理
/// @param frameTime 帧时间
- (IOSurfaceID)bgraCameraTextureReady:(QuarameraShareTexture *)texture
               onScreenTexture:(QuarameraShareTexture *)onScreenTexture
                     frameTime:(NSTimeInterval)frameTime;

@optional

/// 渲染到TargetTexture上可以上屏，如果是GL则需要调用GLFlush来同步
/// @param frameTime frameTime description
/// @param targetTexture targetTexture description
/// @param buffer MTL的CommandBuffer
- (void)externalRender:(NSTimeInterval)frameTime
         targetTexture:(QuarameraShareTexture *)targetTexture
         commandBuffer:(id<MTLCommandBuffer>)buffer;


/// YUV 相机纹理
/// @param yTexture y纹理
/// @param uvTexture yv纹理
- (void)yuvTextureReady:(QuarameraShareTexture *)yTexture uvTexture:(QuarameraShareTexture *)uvTexture;

@end

@interface QuarameraMTLCameraRenderView : MTKView

/// MetalRender
@property (nonatomic, strong, readonly) QuarameraMTLCameraRender *mtlRender;

@property (nonatomic, weak) id<QuarameraMTLCameraRenderViewDelegate> cameraDelegate;

@property (nonatomic) dispatch_queue_t displayRenderQueue;

/// 原始相机纹理 可以快速读取
@property (nonatomic, readonly, strong) QuarameraShareTexture *cameraTexture;
@property (nonatomic, readonly, strong) QuarameraShareTexture *shareTexture;

/// 不带后处理的相机渲染的原始纹理
@property (nonatomic, readonly) CVPixelBufferRef renderTarget;

/// 是否镜像渲染 默认为NO
@property (nonatomic) BOOL needFlip;
  
/// 恢复/开始渲染
- (void)resume;

/// 暂停/挂起渲染
- (void)suspend;

/// 处理相机采集流
/// @param sampleBuffer 相机采集流
- (void)cameraSampleBufferArrive:(CMSampleBufferRef)sampleBuffer;

- (void)addRender:(QuarameraCameraRender *)render;


/// 是否开启Quaramera
/// @param frame frame description
- (instancetype)initWithFrame:(CGRect)frame;

- (instancetype)initWithFrame:(CGRect)frame shareContext:(EAGLContext *)context;

@end
