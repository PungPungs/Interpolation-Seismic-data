#include <stdint.h>
#include <stdlib.h>
#include "header.h"
#include <stdio.h>
#include <Windows.h>
#include <errors.h>
#include <stdbool.h>
#include "endian.h"



bool load_binary(HANDLE hfile, SegyBinaryHeader *binary) {
	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
	DWORD bytesRead;
	bool success = ReadFile(hfile, binary, sizeof(SegyBinaryHeader), &bytesRead, NULL);
	return success && bytesRead == sizeof(SegyBinaryHeader);
}



int main() {
	HANDLE hfile;

	hfile = CreateFile(L"C:\\DEV\\Code\\Python\\Interpolation-Seismic-data\\SB_M2511_03_Test.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hfile == INVALID_HANDLE_VALUE) {
		printf("파일 열기 실패 (%lu)\n", GetLastError());
		return 0;
	}
	SegyBinaryHeader* binary = new SegyBinaryHeader();

	if (binary == NULL) {
		printf("동적 메모리 할당 실패");
		CloseHandle(hfile);
		return 0;
	}

	if (load_binary(hfile, binary) == false) {
		printf("파일 파싱 실패\n");
		return 0;
	}

	int dt = swapEndianInt16(binary->num_of_samples_per_dt);
	//size_t length = (sizeof(SegyTrace) + sizeof(float) * dt);
	//SegyTrace* trace = (SegyTrace*)operator new(length);
	long trace_start = 3600;
	LARGE_INTEGER size;
	GetFileSizeEx(hfile, &size);
	SetFilePointer(hfile, trace_start, NULL, FILE_BEGIN);
	int trace_length = (static_cast<int>(size.QuadPart) - 3600) / ((dt*4) + 240);
	SegyTrace* trace[trace_length] ;
	size_t len = sizeof(SegyTrace) + (sizeof(float) * dt);
	for (int i = 0; i < 13484; i++) {
		trace[i] = (SegyTrace*)operator new(len);
		DWORD bytesRead;
		bool success_2 = ReadFile(hfile, trace[i], (DWORD)len, &bytesRead, NULL);
		if (success_2 == TRUE) {
			trace_start = trace_start + (LONG)len;
			SetFilePointer(hfile, trace_start, NULL, FILE_BEGIN);;
		}
	}

	operator delete (trace);
	delete binary;
	return 0;
}

