
#ifndef IMAGE_H
#define IMAGE_H

#include "image_queue.h"
#include "image_queue.h"

#ifdef __cplusplus
extern "C"
{
#endif
__attribute__((visibility("default"))) __attribute__((used))
void addImageCache(const uint8_t *img, int len, double startX, double startY, double normalWidth, double normalHeight,
                   int width, int height, uint64_t javaTime, uint64_t startT, uint64_t beforeFFi, bool exportFlag);

__attribute__((visibility("default"))) __attribute__((used))
void dispose();
#ifdef __cplusplus
}
#endif

#endif