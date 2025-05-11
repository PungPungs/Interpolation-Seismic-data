from typing import List, Literal
import pandas as pd
import numpy as np
import mmap
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE, METADATA, CONDITION



class Sgy:

    def __init__(self, file_path) -> None:

        # 테스트가 필요할 시 속성 변경
        metadata = METADATA()
        self.BYTE_ORDER = metadata.BYTE_ORDER
        self.EXTENDED_HEADER = metadata.EXTENDED_HEADER
        self.BASE_BYTE = metadata.BASE_BYTE
        self.DATA_TRACE = metadata.DATA_TRACE
        self.VER = metadata.VER

        self.file_path : str = file_path
        with open(self.file_path, "rb") as sgy:
            self.mm = mmap.mmap(sgy.fileno(), 0, access=mmap.ACCESS_READ)
        self.mm.seek(0)

        try:
            self.mm.read(self.BASE_BYTE).decode("ascii")
        except:
            self.mm.read(self.BASE_BYTE).decode("cp500")

        self.mm.seek(self.BASE_BYTE)

        self._binary = pd.DataFrame(columns=["id", "desc","data","ref"])
        self._trace = pd.DataFrame(columns=["id", "desc","data","ref"])
        self._extention = pd.DataFrame(columns=["id", "desc","data","ref"])

        self._binary = self.load_header_to_df(BINARY_HEADER)
        self.ref_issue()
        self.BASE_BYTE = self.BASE_BYTE + 400 + (240 * self.EXTENDED_HEADER)


    def header_to_dataframe(self,mode : Literal["std_trace","ext_trace"]) -> None:
        _header : np.array = None
        if mode == "std_trace":
            _header = STANDARD_BASE_HEADER
            self._trace = self.load_header_to_df(_header)
        elif mode == "ext_trace":
            pass

    def load_header_to_df(self,headers : np.array) -> pd.DataFrame:
        _rows = []
        for _header in headers:
            self.mm.seek(self.BASE_BYTE + _header["id"] - 1)
            _rows.append({
                "id": _header["id"],
                "desc": _header["desc"],
                "data": self.int_from_byte(self.mm.read(_header["len"]), byte_order=self.BYTE_ORDER),
                "ref": _header["ref"],
            })
        return pd.DataFrame(_rows)

    def variable_trace_header(self):
        pass

    def int_from_byte(self, b : bytes, byte_order : Literal["big", "little"] = "big"):
        return int.from_bytes(b, byteorder=byte_order, signed=True)
    
    def ref_issue(self):
        self.endian_conversion() # 3297
        ref = self._binary[self._binary["ref"]].set_index("id")["data"].copy()
        
        ## 속성 확인
        # 확장 헤더 확인
        self.EXTENDED_HEADER = ref.get(305,0)#3521 확인, 예제가 없어 확인 불가
        if self.EXTENDED_HEADER < 0:
            self.EXTENDED_HEADER = self.variable_trace_header() # not fixed

        #데이터 트레이스
        self.DATA_TRACE = ref.get(69,0)
        if self.DATA_TRACE == 0:
            self.DATA_TRACE = ref.get(21,0)

        override_items = {_ref_id : value for _id, _ref_id in CONDITION if(value := ref.get(_id,0)) != 0}

        for key,val in override_items.items():
            ref[key] = val

        self._binary.set_index("id", inplace=True)
        # 판다스 3.0 에서 변경될 문법, 아직 아님
        self._binary["data"].update(ref)
        self._binary.reset_index(inplace=True)

    def endian_conversion(self):
        identifier = self._binary[self._binary["id"] == 97]["data"].iloc[0]
        if identifier == 6730598510:
            self.BYTE_ORDER = "little"
            self._binary = self.load_header_to_df(BINARY_HEADER)
        else:
            self.VER = 1

    def close(self):
        self.mm.close()


'''
1. 일단은 확장 헤더 제외(가변일 경우, 헤더 변환) 작업은 완료
2. 추가적인 상관 관계에 대한 변환은 확인 필요
3. 만약 자료팀의 요구사항이 있다면 A에 맞게 최적화 필요
4. 트레이스의 경우 시각화가 필요한데 이걸 어떻게 처리할지도 확인 필요. 만약 그래픽이 있다면 cuda c를 활용하고 싶은데 어떨지 모르겠네.
5. 트레이스 데이터의 경우 그냥 단일 인지도 확인 필요
________________________________________________

5/11 작업 상황
1. 연관 관계 작업 완료. 부족한 부분 발생 확인을 위하여 추가 데이터 확보
2. seisee 로 데이터 비교하면서 틀린 값 발견 후 보정, 바이트 변환시 unsigned로 인하여 값 에러 발생
'''


if __name__ == "__main__":
    sgy = Sgy(r"C:\dev\Code\Interpolation-Seismic-data\SB_M2511_03_Test_Header.sgy")
    sgy.header_to_dataframe("std_trace")
    print(sgy.load_trace_data_to_df())
    sgy.close()