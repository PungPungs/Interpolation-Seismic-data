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
                "data": self.int_from_byte(self.mm.read(_header["len"]), self.BYTE_ORDER),
                "ref": _header["ref"],
            })
        return pd.DataFrame(_rows)



    # 데이터가 -1 인 경우 가변, ㄴㄴ데이터의 처리 방법을 생각해야함
    def variable_trace_header(self):
        pass

    def int_from_byte(self, b : bytes ,byte_order : Literal["big", "little"] = "big"):
        return int.from_bytes(b, byteorder=byte_order)
    
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
1. 변경 필요한 확인 후 적용하는 함수 설계 필요
2. 확장 헤더가 있을 경우의 헤더 시작점 설정

# over the ver2
    big = 1690906010 or little = 6730598510 -> byte_order
# under the ver2
    0 and big endian
'''


if __name__ == "__main__":
    sgy = Sgy(r"C:\dev\Code\Interpolation-Seismic-data\SB_M2511_03_Test.sgy")
    print(sgy._binary)
    