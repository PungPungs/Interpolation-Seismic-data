#include <stdint.h>
#include <stdlib.h>
#include <iostream>
#include "header.h"
#include <stdio.h>
#include <Windows.h>
#include <errors.h>
#include <stdbool.h>
#include "endian.h"
#include <chrono>
#include "vector"
#include <memory>

using namespace std;
void getTrace(BYTE* bytes, int ch, int length) {
	SegyTrace* trace = reinterpret_cast<SegyTrace*>(bytes + (length * ch));
}
int main() {
	HANDLE hfile;

	hfile = CreateFile(L"C:\\DEV\\Code\\Interpolation-Seismic-data\\SB_M2511_03_Test.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hfile == INVALID_HANDLE_VALUE) {
		//MessageBox(NULL, L"FIle Open Failed", L"Error", MB_OK);
		cout << "failed" << endl;
		return -1;
	}

	SegyBinaryHeader* binary = new SegyBinaryHeader();
	DWORD readByte;
	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
	bool success = ReadFile(hfile, binary, sizeof(SegyBinaryHeader), &readByte, NULL);
	if (success && readByte != sizeof(SegyBinaryHeader)) {
		return -1;
	}

	int16_t numOfSamples = swapEndianInt16(binary->num_of_samples_per_dt);
	int32_t channel = swapEndianInt32(binary->reel_number);

	size_t fileSize = 0;
	int32_t traceLength = 240 + (numOfSamples * sizeof(float));

	if (channel == 0) {
		LARGE_INTEGER size;
		GetFileSizeEx(hfile, &size);
		fileSize = size.QuadPart;
		channel = (fileSize - 3600) / traceLength;
	}
	auto start = chrono::steady_clock::now();

	//SetFilePointer(hfile, 3600, NULL, FILE_BEGIN);
	//BYTE* bytes = (BYTE*)malloc(fileSize - 3600);
	//bool successed = ReadFile(hfile, bytes, (fileSize - 3600), &readByte, NULL);
	//if (successed && readByte != fileSize - 3600) {
	//	return -1;
	//}
	//for (int i = 0; i < channel; i++) {
	//	getTrace(bytes, i, traceLength);
	//}
	long offset = 3600;
	SegyTrace** ptr_trace = new SegyTrace * [channel];
	for (int i = 0; i < channel; i++) {
		SetFilePointer(hfile, offset, NULL, FILE_BEGIN);
		ptr_trace[i] = (SegyTrace*)malloc(traceLength);
		bool successed = ReadFile(hfile, ptr_trace[i], traceLength, &readByte, NULL);
		offset += traceLength;
	}

	auto end = chrono::steady_clock::now();
	chrono::duration<double>milli = end - start;
	std::cout << "파일 읽기 시간: " << chrono::duration<double>(end - start).count() << "초\n";

	CloseHandle(hfile);
	delete binary;

	return 0;
}
