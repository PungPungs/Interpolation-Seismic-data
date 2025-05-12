from typing import List, Literal, Optional
import pandas as pd
import numpy as np
import mmap
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE, METADATA, CONDITION
from math import isclose
from pprint import pprint


class Sgy:

    def __init__(self, file_path) -> None:

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
        except:
            pprint(self.mm.read(self.BASE_BYTE).decode("cp500"))

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
        self.FORMAT_CODE = [row["format"],row["byte"]]

    def close(self):
        self.mm.close()

######################################
#              test part             #
######################################
    # 코드별 상관 관계 설정
    def read_trace_data(self) -> np.ndarray:
        _endian = '>' if self.BYTE_ORDER == "big" else '<'

        _ndtype = (_endian + self.FORMAT_CODE[0]).item()
        _byte_size = self.FORMAT_CODE[1].item()
        _data_trace = (self.DATA_TRACE * _byte_size).item()
        _total = ((self.TOTAL_SIZE - self.BASE_BYTE) / (_data_trace + 240)).item()
        print(_total)
        if isclose(_total % 1, 0.0):
            _total = int(_total)
        else:
            raise ValueError(f"trace 길이 불일치: 총 길이={self.TOTAL_SIZE}, 예상={_total}")
        
        traces = np.empty((_total, self.DATA_TRACE), dtype=_ndtype)

        for idx in range(_total):
            _base = (self.BASE_BYTE + idx * (240 + _data_trace))
            self.mm.seek(_base + 240)
            traces[idx] = np.frombuffer(self.mm.read(_data_trace),_ndtype)
        return traces



'''
1. 일단은 확장 헤더 제외(가변일 경우, 헤더 변환) 작업은 완료 .A의 경우 확장 헤더 사용하진 않지만 일단 설정만 해두는걸로
2. 추가적인 상관 관계에 대한 변환은 확인 필요 (포멧 코드, 에디안 등은 완료)
3. 만약 자료팀의 요구사항이 있다면 A에 맞게 최적화 필요
4. 트레이스의 경우 시각화가 필요한데 이걸 어떻게 처리할지도 확인 필요.
5. 자료를 시간에 맞춰서 순서를 잡는데, 만약 4채널일 경우 입력 4개 출력이 4개 필요, 만약 11168이면 11168이 필요한 것
    1. 인위적으로 맞추는 건 즉 시간에 따른 시작점을 잡는건데 동시 다발적으로 들어가서 행렬곱을 수행하면 어차피 모든 상관 관계를 확인하는거니까 문제는 없을 듯
    2. 다른 참조 사항이 있으면 이건 어떻게 설정해주는거냐인데...
6. 라인수가 몇 개 인지 넘겨야한다는 점도 확인 필요
________________________________________________

5/11 작업 상황
1. 바이너리 헤더, 트레이스 헤더, 트레이스 데이터 전부 넘파이를 이용하여 텍스트화 완료. A에서 따로 csv는 필요 없다고 하여 패스. 용량이 3배 증가
2. 이제 attention or 일반 신경망을 이용하여 피킹값 예측 필요
'''


if __name__ == "__main__":
    sgy = Sgy(r"241115_073433_795565.sgy")
    sgy.header_to_dataframe("std_trace")
    sgy.close()