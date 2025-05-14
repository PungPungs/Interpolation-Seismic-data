import numpy as np
import mmap
import pandas as pd
import struct
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE
from typing import Literal, Tuple, List, Union

class SEGYReader:
    TEXT_HEADER_END = 3200
    BINARY_HEADER_LENGTH = 400
    TRACE_HEADER_LENGTH = 240
    TRACE_START = 3600
    signed_fmt : dict[int,str] = {
        1: 'b',
        2: 'h',
        4: 'i',
        6: 'hi',
        8: 'q',
    }



    read_header : dict[str,List] = {
        "text": [0, TEXT_HEADER_END],
        "binary": [TEXT_HEADER_END, BINARY_HEADER_LENGTH],
        "trace": [TRACE_START, TRACE_HEADER_LENGTH],
    }

    def __init__(self, file_path):
        np.set_printoptions(suppress=True)
        self.file_path = file_path
        self.text_header = ""
        self.binary_header = pd.DataFrame()
        self.trace_header = pd.DataFrame()
        self.encoding = "ascii"

        with open(self.file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # 정보 취득을 위한 기본 헤더 읽기 : 필수
        self._read_headers()
        # 이후 기타 세팅을 위한 정보 읽기 : 필수
        self.extract_features()
        self.read_trace()

    def _read_headers(self):
        for key, (start, size) in self.read_header.items():
            self.mm.seek(start)
            data = self.mm.read(size)
            if key == "text":
                self.text_header, self.encoding = self._decode_text(data)
            else:
                header_list = self._parse_header(data, key)
                if key == "binary":
                    self.binary_header = pd.DataFrame(header_list)
                elif key == "trace":
                    self.trace_header = pd.DataFrame(header_list)

    def _decode_text(self, b: bytes):
        try:
            return b.decode("ascii"), "ascii"
        except UnicodeDecodeError:
            return b.decode("cp500"), "cp500"

    def _parse_header(self, b: bytes, kind: Literal["binary", "trace"]):
        header_def = BINARY_HEADER if kind == "binary" else STANDARD_BASE_HEADER
        rows = []
        for h in header_def:
            fmt = self.signed_fmt.get(h["len"])
            if fmt:
                val = struct.unpack_from(f">{fmt}", b, h["id"] - 1)[0]
                rows.append({
                    "id": h["id"],
                    "desc": h["desc"],
                    "data": val,
                })
        return pd.DataFrame(rows)

    def extract_features(self):
        # 1st 트레이스 헤더
        self.num_of_sample = self.trace_header[self.trace_header["id"] == 115]["data"].item()
        self.interval = self.trace_header[self.trace_header["id"] == 117]["data"].item()
        _fmt = self.binary_header[self.binary_header["id"] == 25]["data"].item()
        _fmt_data = SAMPLING_CODE[SAMPLING_CODE["code"] == _fmt]
        self.trace_format = _fmt_data["format"].item()
        self.trace_format_size = _fmt_data["byte"].item()

        if self.interval != 0:
            self.time_index = np.arange(0, self.num_of_sample) * (self.interval / 1000)
            print(self.time_index)
        
    def read_trace(self):
        self.total_size = self.mm.size()
        step = 240 + self.num_of_sample * 4
        trace_data_size = self.total_size - self.TRACE_START

        if step <= 0:
            return None

        if trace_data_size % step != 0:
            raise ValueError("트레이스 길이가 맞지 않습니다.")
        self.channel = trace_data_size // step

        self.mm.seek(self.TRACE_START)
        b = self.mm.read(trace_data_size)
        self.trace_header, self.samples = self.split_trace_data(b)
    
    # numpy 배열로 받고 필요할 때 마다 라인별로 읽기
    def split_trace_data(self, b : bytes) -> Tuple[np.ndarray, np.ndarray]:
        step = self.TRACE_HEADER_LENGTH + self.num_of_sample * self.trace_format_size
        raw = np.frombuffer(b, dtype=np.uint8).reshape((-1, step))
        header = raw[:, :self.TRACE_HEADER_LENGTH]
        sample =  raw[:, self.TRACE_HEADER_LENGTH:]
        return header, sample
        

    def all_parse_sample(self,b : np.ndarray):
        return np.frombuffer(b.tobytes(), dtype= f">{self.trace_format}").reshape((-1, self.num_of_sample))
    

    def stream_trace_header(self, ch : int, to_csv : bool = False) -> pd.DataFrame:
        end_line = len(self.trace_header)
        if ch == 0 or ch == end_line:
            raise ValueError(f"trace 범위 : 1 ~ {end_line}")
        _data = self.trace_header[ch-1]
        line_header = self._parse_header(_data,'trace')
        if to_csv == True:
            line_header.to_csv(f"line_{ch}.csv")
        return line_header
    
    def stream_trace_data(self, ch : int, to_csv : bool):
        pass
### 작업 전
    def all_parse_header(self,b : np.ndarray):
        row = []
        for _b in b:
            row.append(self._parse_header(_b.tobytes(), 'trace'))

'''
### 추가 작업 필요 사항
코드 별 포멧 확인
'''

            
a = SEGYReader(r"SB_M2511_03_Test_Header.sgy")
print((a.trace_header))
print((a.stream_trace_header(4, True)))