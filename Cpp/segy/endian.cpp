#include "endian.h"
#include <cstdint>
#include <cstring>
#include <iostream>

float swapEndianFloat32(float input) {
	uint32_t raw;
	std::memcpy(&raw, &input, sizeof(float));  // float -> uint32_t (bit pattern 복사)

	// 바이트 순서 변경 (정석적인 비트 연산 방식)
	raw = ((raw & 0x000000FF) << 24) |
		((raw & 0x0000FF00) << 8) |
		((raw & 0x00FF0000) >> 8) |
		((raw & 0xFF000000) >> 24);

	float result;
	std::memcpy(&result, &raw, sizeof(float));  // uint32_t -> float
	return result;
}

int32_t swapEndianInt32(int32_t value) {
	uint32_t u = static_cast<uint32_t>(value);

	u = ((u & 0x000000FF) << 24) |
		((u & 0x0000FF00) << 8) |
		((u & 0x00FF0000) >> 8) |
		((u & 0xFF000000) >> 24);

	return static_cast<int32_t>(u);
}

int16_t swapEndianInt16(int16_t value) {
	uint16_t u = static_cast<uint16_t>(value);

	u = ((u & 0x00FF) << 8) |
		((u & 0xFF00) >> 8);

	return static_cast<int16_t>(u);
}