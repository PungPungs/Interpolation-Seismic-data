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
////SegyTrace* trace = (SegyTrace*)operator new(length);
////SegyTrace* trace[trace_length] ;
////size_t len = sizeof(SegyTrace) + (sizeof(float) * dt);
////for (int i = 0; i < 13484; i++) {
////	trace[i] = (SegyTrace*)operator new(len);
////	DWORD bytesRead;
////	bool success_2 = ReadFile(hfile, trace[i], (DWORD)len, &bytesRead, NULL);
////	if (success_2 == TRUE) {
////		trace_start = trace_start + (LONG)len;
////		SetFilePointer(hfile, trace_start, NULL, FILE_BEGIN);;
////	}
////}
//
//bool load_binary(HANDLE hfile, SegyBinaryHeader* binary) {
//	SetFilePointer(hfile, 3200, NULL, FILE_BEGIN);
//	DWORD bytesRead;
//	bool success = ReadFile(hfile, binary, sizeof(SegyBinaryHeader), &bytesRead, NULL);
//	return success && bytesRead == sizeof(SegyBinaryHeader);
//}
//
//void getTrace(BYTE* bytes, int ch, int length) {
//	SegyTrace* trace = reinterpret_cast<SegyTrace*>(bytes + (length * ch));
//}
//
//int main() {
//	HANDLE hfile;
//
//	hfile = CreateFile(L"C:\\DEV\\Code\\Interpolation-Seismic-data\\SB_M2511_03_Test.sgy", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
//	if (hfile == INVALID_HANDLE_VALUE) {
//		printf("���� ���� ���� (%lu)\n", GetLastError());
//		return 0;
//	}
//	SegyBinaryHeader* binary = new SegyBinaryHeader();
//
//	if (binary == NULL) {
//		printf("���� �޸� �Ҵ� ����");
//		CloseHandle(hfile);
//		return 0;
//	}
//
//	if (load_binary(hfile, binary) == false) {
//		printf("���� �Ľ� ����\n");
//		return 0;
//	}
//
//	int dt = swapEndianInt16(binary->num_of_samples_per_dt);
//	size_t length = sizeof(SegyTrace) + (sizeof(float) * dt);
//
//
//	long trace_start = 3600;
//	LARGE_INTEGER size;
//	GetFileSizeEx(hfile, &size);
//	long trace_size = size.QuadPart - 3600;
//	uint16_t channel = (size.QuadPart - 3600) / length;
//	DWORD readBytes;
//
//
//	auto start = std::chrono::steady_clock::now();
//
//	vector<SegyTrace> trace(channel);
//	for (int i = 0; i < channel; i++) {
//		long offset = trace_start + (length * i);
//		SetFilePointer(hfile, offset, NULL, FILE_BEGIN);
//		bool successed = ReadFile(hfile, &trace[i], length, &readBytes, NULL);
//		if (successed && readBytes != length) {
//			printf("false\n");
//		}
//	}
//	auto end = std::chrono::steady_clock::now();
//	chrono::duration<double>milli = end - start;
//	std::cout << "���� �б� �ð�: " << std::chrono::duration<double>(end - start).count() << "��\n";
//
//
//	return 0;
//}
