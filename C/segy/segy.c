#include <stdint.h>
#include <stdlib.h>
#include "header.h"
#include <stdio.h>
#include <Windows.h>
#include <errors.h>
#include <stdbool.h>
#include "endian.h"

int16_t swap16(int16_t x) {
	return (x >> 8) | (x << 8);
}

int32_t swap32(int32_t x) {
	return (x >> 24) & 0x000000FF |
		(x >> 8) & 0x0000FF00 |
		(x << 8) & 0x00FF0000 |
		(x << 24) & 0xFF000000;
}

bool load_binary(HANDLE hfile, SegyBinaryHeader *binary) {
	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
	DWORD bytesRead;
	bool success = ReadFile(hfile, binary, sizeof(SegyBinaryHeader), &bytesRead, NULL);
	return success && bytesRead == sizeof(SegyBinaryHeader);
}

int main() {
	HANDLE hfile;

	hfile = CreateFile(L"C:\\dev\\Code\\Interpolation-Seismic-data\\241115_073433_795565.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hfile == INVALID_HANDLE_VALUE) {
		printf("파일 열기 실패 (%lu)\n", GetLastError());
		return 0;
	}
	SegyBinaryHeader *binary = (SegyBinaryHeader *)malloc(sizeof(SegyBinaryHeader));
	if (binary == NULL) {
		printf("동적 메모리 할당 실패");
		CloseHandle(hfile);
		return 0;
	}

	if (load_binary(hfile, binary) == false) {
		printf("파일 파싱 실패\n");
		return 0;
	}

	//DWORD bytesRead;
	//SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
	//bool success = ReadFile(hfile, &binary, sizeof(binary), &bytesRead, NULL);
	//SegyTrace* trace = malloc(sizeof(SegyTrace) + sizeof(float) * 100);

	printf("%d\n", swap16(binary->revesion_number));
	printf("%d\n", swap16(binary->fixed_length_trace_flag));
	printf("%d\n", swap16(binary->sample_interval));

	CloseHandle(hfile);
	free(binary);


	return 0;
}

