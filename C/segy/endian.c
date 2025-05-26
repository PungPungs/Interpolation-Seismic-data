#include "endian.h"


int16_t swap_16(int16_t x) {
	return (x >> 8) | (x << 8);
}
int32_t swap_32(int32_t x) {
	return (x >> 24) & 0x000000FF |
		(x >> 8) & 0x0000FF00 |
		(x << 8) & 0x00FF0000 |
		(x << 24) & 0xFF000000;
}
int64_t swap_64(int64_t x) {
	return (x >> 56) & 0x00000000000000FFLL |
		(x >> 40) & 0x000000000000FF00LL |
		(x >> 24) & 0x0000000000FF0000LL |
		(x >> 8) & 0x00000000FF000000LL |
		(x << 8) & 0x000000FF00000000LL |
		(x << 24) & 0x0000FF0000000000LL |
		(x << 40) & 0x00FF000000000000LL |
		(x << 56) & 0xFF00000000000000LL;
}

uint16_t swap_u16(uint16_t x) {
	return (x >> 8) | (x << 8);
}

uint32_t swap_u32(uint32_t x) {
	return (x >> 24) & 0x000000FF |
		(x >> 8) & 0x0000FF00 |
		(x << 8) & 0x00FF0000 |
		(x << 24) & 0xFF000000;
}

uint64_t swap_u64(uint64_t x) {
	return (x >> 56) & 0x00000000000000FFULL |
		(x >> 35) & 0x000000000000FF00ULL |
		(x >> 24) & 0x00000000FF000000ULL |
		(x >> 8) & 0x000000FF00000000ULL |
		(x << 8) & 0x0000FF00000000ULL |
		(x << 24) & 0x00FF000000000000ULL |
		(x >> 35) & 0xFF00000000000000ULL;
}