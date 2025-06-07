//#include <stdint.h>
//#include <stdlib.h>
//#include <iostream>
//#include "header.h"
//#include <stdio.h>
//#include <Windows.h>
//#include <errors.h>
//#include <stdbool.h>
//#include "endian.h"
//#include <chrono>
//#include "vector"
//using namespace std;
//
//int main() {
//	HANDLE hfile;
//
//	hfile = CreateFile(L"C:\\DEV\\Code\\Interpolation-Seismic-data\\SB_M2511_03_Test.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
//	if (hfile == INVALID_HANDLE_VALUE) {
//		//MessageBox(NULL, L"FIle Open Failed", L"Error", MB_OK);
//		cout << "failed" << endl;
//		return -1;
//	}
//
//	SegyBinaryHeader* binary = new SegyBinaryHeader();
//	DWORD readByte;
//	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
//	bool success = ReadFile(hfile, binary, sizeof(SegyTrace), &readByte, NULL);
//	if (success && readByte != sizeof(SegyTrace)) {
//		return -1;
//	}
//
//
//
//	int16_t numOfSamples = swapEndianInt16(binary->num_of_samples_per_dt);
//	int32_t channel = swapEndianInt32(binary->reel_number);
//
//	size_t fileSize = 0;
//	int32_t traceLength = 240 + (numOfSamples * sizeof(float));
//
//	if (channel == 0) {
//		LARGE_INTEGER size;
//		GetFileSizeEx(hfile, &size);
//		fileSize = size.QuadPart;
//		channel = (fileSize - 3600) / traceLength;
//	}
//	auto start = std::chrono::steady_clock::now();
//
//	vector<SegyTrace*> trace(channel);
//	long offset = 3600;
//	for (int i = 0; i < channel; i++) {
//		trace[i] = (SegyTrace*)malloc(traceLength);
//		SetFilePointer(hfile, offset, NULL, FILE_BEGIN);
//		bool successed = ReadFile(hfile, trace[i], traceLength, &readByte, NULL);
//		if (successed && readByte != traceLength) {
//			printf("false\n");
//		}
//		offset += traceLength;
//	}
//
//	auto end = std::chrono::steady_clock::now();
//	chrono::duration<double>milli = end - start;
//	std::cout << "파일 읽기 시간: " << std::chrono::duration<double>(end - start).count() << "초\n";
//
//	CloseHandle(hfile);
//	delete binary;
//
//	return 0;
//}
