
#ifndef ENDIANNESS_H
#define ENDIANNESS_H

#include "stdint.h"

#pragma once

float swapEndianFloat32(float input);
int32_t swapEndianInt32(int32_t value);
int16_t swapEndianInt16(int16_t value);

#endif