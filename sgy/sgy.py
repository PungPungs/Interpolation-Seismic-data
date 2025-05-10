from typing import List, Literal
import pandas as pd
import numpy as np
import mmap
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE



class Sgy:
    BASE_BYTE = 3200
    EXTENDED_HEADER = 0

    def __init__(self, file_path) -> None:
        self.file_path : str = file_path
        with open(self.file_path, "rb") as sgy:
            self.mm = mmap.mmap(sgy.fileno(), 0, access=mmap.ACCESS_READ)
        self.mm.seek(0)
        print(self.mm.read(3200).decode("ascii"))
        self.mm.seek(self.BASE_BYTE)
        self._summary = pd.DataFrame(columns=["id", "desc","data","ref"])

    def header_to_datafrmae(self,mode : Literal["binary","std_trace","ext_trace"]) -> pd.DataFrame:
        _header : np.array = []
        _rows : list = []

        if mode == "binary":
            _header = BINARY_HEADER
        elif mode == "std_trace":
            _header = STANDARD_BASE_HEADER
        # if mode == "ext_trace":
        #     _header = BINARY_HEADER           
        if  len(_header) == 0:
                raise ValueError("No header files")
        
        for header in _header:
            self.mm.seek(self.BASE_BYTE + header["id"] - 1)
            _rows.append({
                "id": header["id"],
                "desc": header["desc"],
                "data": int.from_bytes(self.mm.read(header["len"])),
                "ref": header["ref"],
            })

        self._summary = pd.DataFrame(_rows)
        print(self._summary)

    def ref_issue(self):
        ref = self._summary[self._summary["ref"]]
    # {"id" : 3297, "data" : 0, "ref_id" : 3223}, #edian
        self.EXTENDED_HEADER = ref[ref["id"] == 3505]["data"]

    def close(self):
        self.mm.close()
'''
1. 변경 필요한 확인 후 적용하는 함수 설계 필요
2. 확장 헤더가 있을 경우의 헤더 시작점 설정
'''


if __name__ == "__main__":
    sgy = Sgy(r"C:\dev\Code\Interpolation-Seismic-data\SB_M2511_03_Test.sgy")
    sgy.header_to_datafrmae('binary')
    sgy.ref_issue()