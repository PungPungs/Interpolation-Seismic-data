from typing import List, Literal, Optional
import pandas as pd
import numpy as np
import mmap
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE, METADATA, CONDITION
from math import isclose
from pprint import pprint


class Sgy:

    def __init__(self, file_path) -> None:
        np.set_printoptions(suppress=True)
        # 테스트가 필요할 시 속성 변경
        metadata = METADATA()
        self.BYTE_ORDER = metadata.BYTE_ORDER
        self.EXTENDED_HEADER = metadata.EXTENDED_HEADER
        self.BASE_BYTE = metadata.BASE_BYTE
        self.DATA_TRACE = metadata.DATA_TRACE
        self.VER = metadata.VER
        self.TOTAL_SIZE = None
        self.file_path : str = file_path
        self.FORMAT_CODE = []


        with open(self.file_path, "rb") as sgy:
            self.mm = mmap.mmap(sgy.fileno(), 0, access=mmap.ACCESS_READ)
            self.TOTAL_SIZE = self.mm.size()
        self.mm.seek(0)

        try:
            pprint(self.mm.read(self.BASE_BYTE).decode("ascii"))
        except UnicodeDecodeError:
            self.mm.seek(0)
            pprint(self.mm.read(self.BASE_BYTE).decode("cp500"))

        self.mm.seek(self.BASE_BYTE)

        self._binary = pd.DataFrame(columns=["id", "desc","data","ref"])
        self._trace = pd.DataFrame(columns=["id", "desc","data","ref"])
        self._extention = pd.DataFrame(columns=["id", "desc","data","ref"])
        self._trace_data = pd.DataFrame(columns=["idx","time (ms)","sample"])

        self._binary = self.load_header_to_df(BINARY_HEADER)
        self.ref_issue()
        self.BASE_BYTE = self.BASE_BYTE + 400 + (240 * self.EXTENDED_HEADER)
        self._trace = self.load_header_to_df(STANDARD_BASE_HEADER)
        _temp = self.load_trace_data_to_df(self.read_trace_data())
        print(_temp)

    def load_trace_data_to_df(self, nd: pd.DataFrame):
        rows = []
        _ndtype = self.FORMAT_CODE
        temp = np.arange(0,len(nd.T),dtype=_ndtype)
        temp *= self.interval
        for i in range(len(temp)):
            rows.append({
                "index": i,
                "time (ms)": temp[i],
            })
        return pd.DataFrame(rows).join(nd.T)

    def header_to_dataframe(self,mode : Literal["std_trace","ext_trace"]) -> None:
        _header : np.array = None
        if mode == "std_trace":
            _header = STANDARD_BASE_HEADER
            self._trace = self.load_header_to_df(_header)
        elif mode == "ext_trace":
            pass


    ### 추후 고민(전체를 읽고 슬라이싱 or 현 상태 유지)
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
        self.set_format()
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
        self.interval = int(self._binary[self._binary["id"] == 17]["data"].item()) / 1000


    def endian_conversion(self):
        identifier = self._binary[self._binary["id"] == 97]["data"].iloc[0]
        if identifier == 6730598510:
            self.BYTE_ORDER = "little"
            self._binary = self.load_header_to_df(BINARY_HEADER)
        else:
            self.VER = 1

    def set_format(self) -> None:
        format_type = self._binary[self._binary["id"] == 25]["data"].iloc[0]
        row = SAMPLING_CODE[SAMPLING_CODE['code'] == format_type]
        self.FORMAT_CODE = row["format"].item()
        self.FORMAT_SIZE = row["byte"].item()

    def close(self):
        self.mm.close()

######################################
####          test part           ####
######################################
    # 코드별 상관 관계 설정
    def read_trace_data(self) -> np.ndarray:
        rows = []
        _endian = '>' if self.BYTE_ORDER == "big" else '<'
        _ndtype = _endian + self.FORMAT_CODE
        _byte_size = self.FORMAT_SIZE
        _data_trace = (self.DATA_TRACE * _byte_size)
        _total = ((self.TOTAL_SIZE - self.BASE_BYTE) / (_data_trace + 240))
        if isclose(_total % 1, 0.0):
            _total = int(_total)
        else:
            raise ValueError(f"trace 길이 불일치: 총 길이={self.TOTAL_SIZE}, 예상={_total}")
    
        for idx in range(_total):
            _base = (self.BASE_BYTE + idx * (240 + _data_trace))
            self.mm.seek(_base + 240)
            rows.append(np.frombuffer(self.mm.read(_data_trace),_ndtype))
        return pd.DataFrame(rows)



'''
### 최종 목적
1. 피킹 : 오토 피킹, 수 많은 물리학자들이 시도하였고 다양한 방법이 있겠지만 나라고 못할끼? 나도 할 수 있다.
________________________________________________
### 문제점
1. 코드가 너무 난잡한 거 같다. 이걸 버전 1로 두고 버전 2를 개발해야하는지 아니면 바로 리펙토링을 할지 모르겠다. 분명히 공부는 되기는 하였으나 너무 복잡하게 얽혀있다.
2. 각각의 객체가 책임을 많이 진다. 또한 너무 응집도가 강해 하나 수정시 전체가 영향을 받을 듯 하다.
3. 너무 쓸모 없는 변수들의 생성과 효율적이지 않는 구조 같다. 1번과 같이 고려하여 생각해보자
3. 너무 쓸모 없는 변수들의 생성과 효율적이지 않는 구조 같다. 1번과 같이 고려하여 생각해보자
________________________________________________

5/11 작업 상황
1. 바이너리 헤더, 트레이스 헤더, 트레이스 데이터 전부 넘파이를 이용하여 텍스트화 완료. A에서 따로 csv는 필요 없다고 하여 패스. 용량이 3배 증가
2. 이제 attention or 일반 신경망을 이용하여 피킹값 예측 필요

'''


if __name__ == "__main__":
    sgy = Sgy(r"241115_073433_795565.sgy")
    sgy.close()