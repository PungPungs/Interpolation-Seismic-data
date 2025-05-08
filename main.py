import os
import struct
from config import Seg_y_Rev2_1_Config

HEADER = 3200
BINARY = 400
TRACE = 240


'''
# data trace index -> 0 ~ 239
trace
3600 + 0 ~ 4 byte -> 트레이스의 번호
3502 ~ 3053 -> 샘플링 고정 여부
'''
def main():

    BINARY_FILE_HEADER = Seg_y_Rev2_1_Config.BINARY_FILE_HEADER
    path = "SB_M2511_03_Test_Header.sgy"
    file_size = os.path.getsize(path)
    print(f"{file_size}bytes..")
    if (file_size == 0):
        print("파일 크기 0byte.. 읽을 수 없음")



    with open(path, "rb") as f:
        f.seek(0)
        for key in BINARY_FILE_HEADER:
            f.seek(key - 1) # idx starts with 0
            value = BINARY_FILE_HEADER.get(key)
            print(key, value[0], int.from_bytes(f.read(value[1])))

# 확장 헤더 확인
def num_of_additional_trace_header(header : int) -> bool:
    '''additional header'''
    if header != 0:
        return header
    else:
        False 


        




if __name__ == "__main__":
    main()