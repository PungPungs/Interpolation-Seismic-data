#include <stdint.h>
#include <stdlib.h>
#include "header.h"
#include <stdio.h>
#include <Windows.h>
#include <errors.h>
#include <stdbool.h>

int16_t swap(int16_t x) {
	return (x >> 8) | (x << 8);
}

bool load_binary(HANDLE hfile, SegyBinaryHeader* binary) {
	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
	DWORD bytesRead;
	bool success = ReadFile(hfile, &binary, sizeof(binary), &bytesRead, NULL);
	return success && bytesRead == sizeof(SegyBinaryHeader);
}

int main() {
	HANDLE hfile = NULL;

	hfile = CreateFile(L"C:\\dev\\Code\\Interpolation-Seismic-data\\sgy\\241115_073433_795565.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hfile == INVALID_HANDLE_VALUE) {
		printf("파일 열기 실패 (%lu)\n", GetLastError());
		return 0;
	}
	SegyBinaryHeader binary;


	//SegyTrace* trace = malloc(sizeof(SegyTrace) + sizeof(float) * 100);
	printf("%d\n", swap(binary.revesion_number));
	printf("%d\n", swap(binary.fixed_length_trace_flag));


	return 0;
}

