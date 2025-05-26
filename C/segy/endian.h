
#ifndef ENDIANNESS_H
#define ENDIANNESS_H

#include "stdint.h"

#pragma once

int16_t swap_16(int16_t x);
int32_t swap_32(int32_t x);
int64_t swap_64(int64_t x);
uint16_t swap_u16(uint16_t x);
uint32_t swap_u32(uint32_t x);
uint64_t swap_u64(uint64_t x);

#endif