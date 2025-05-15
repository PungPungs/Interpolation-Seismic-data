import numpy as np
import mmap
import pandas as pd
import struct
from header import BINARY_HEADER, STANDARD_BASE_HEADER, SAMPLING_CODE
from typing import Literal, Tuple, List, Union
import re

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
    n_signed_fmt : dict[int,str] = {
        1: 'i',
        2: 'i2',
        4: 'i4',
        8: 'i8',
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
        self.total_size = 0
        self.encoding = "ascii"
        self.channel : int = 0
        self.time_index : List = []
        self.interval : int = 0
        self.total_size : int = 0
        self.num_of_sample : int = 0

        self.binary_header = pd.DataFrame()
        self.bin_trace_header : bytes
        self.bin_trace_samples : bytes

        with open(self.file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.total_size = self.mm.size()
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

    # 바꿔야겠다. 넘파이 방식으로
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
        
    def read_trace(self):
        step = 240 + self.num_of_sample * self.trace_format_size
        trace_data_size = self.total_size - self.TRACE_START
        if step <= 0:
            return None
        if trace_data_size % step != 0:
            raise ValueError("트레이스 길이가 맞지 않습니다.")
        self.channel = trace_data_size // step
        self.mm.seek(self.TRACE_START)
        b = self.mm.read(trace_data_size)
        self.bin_trace_header, self.bin_trace_samples = self.split_trace_data(b)
    
    # numpy 배열로 받고 필요할 때 마다 라인별로 읽기
    def split_trace_data(self, b : bytes) -> Tuple[np.ndarray, np.ndarray]:
        step = self.TRACE_HEADER_LENGTH + self.num_of_sample * self.trace_format_size
        raw = np.frombuffer(b, dtype=np.uint8).reshape((-1, step))
        header = raw[:, :self.TRACE_HEADER_LENGTH]
        sample =  raw[:, self.TRACE_HEADER_LENGTH:]
        return header, sample

    def stream_trace_header(self, ch : int, to_csv : bool = False) -> pd.DataFrame:
        end_line = len(self.bin_trace_header)
        if ch <= 0 or ch > end_line:
            raise ValueError(f"trace 범위 : 1 ~ {end_line}")
        _data = self.bin_trace_header[ch-1]
        line_header = self._parse_header(_data,'trace')
        if to_csv == True:
            line_header.to_csv(f"line_{ch}.csv")
        return line_header
    
    def stream_trace_data(self, ch : int, to_csv : bool) -> pd.DataFrame:
        end_line = len(self.bin_trace_samples)
        idx = ch - 1
        if ch <= 0 or ch > len(end_line):
            raise ValueError(f"trace 범위 : 1 ~ {end_line}")
        sample = (self.bin_trace_samples[idx])
        line_trace = np.frombuffer(sample,dtype=f">{self.trace_format}")
        temp = pd.DataFrame({
            "Time(ms)" : self.time_index, 
            "Sample" : line_trace
            }, dtype=f"float32")
        temp.index += 1
        if to_csv == True:
            temp.to_csv(f"trace{ch}.csv")
        return temp
        


    def info(self) -> pd.DataFrame:
        metadata = {
            "file_path" : self.file_path,
           "total_size" : self.total_size,
            "text_header" : self.text_header,
            "total_size" : self.total_size,
            "encoding" : self.encoding ,
            "channel" : self.channel,
           "time_index" : self.time_index,
           "interval" : self.interval,
           "num_of_sample": self.num_of_sample,
        }
        return pd.DataFrame(metadata)

    def parse_text_header(self):
        parse_data = (re.split(r"(?=C\s?\d?\d)", self.text_header))
        return pd.DataFrame({"3200-byte Textual File Header" : parse_data})
    
    def load_all_header(self, b : np.ndarray) -> pd.DataFrame:
        row = []
        header_def = STANDARD_BASE_HEADER
        for h in header_def:
            start = h["id"].item() - 1
            end = start + h["len"]
            fmt = self.n_signed_fmt.get(h["len"])
            if fmt == None:
                row.append([[],[],[],[]])
                continue
            row.append(np.frombuffer(b[:, start:end].tobytes(), dtype=f">{fmt}"))
            idx = [f"ch_{_}" for _ in range(1,self.channel + 1)]
        return pd.DataFrame(row, columns=idx).to_csv("tester.csv")

    def load_all_data(self, b : np.ndarray) -> pd.DataFrame:
        '''데이터가 클수록 오래 걸림'''
        row = []
        row.append(np.frombuffer(b.tobytes(),dtype=f">{self.trace_format}"))
        return pd.DataFrame(row)

'''

### 추가 작업 필요 사항
코드 별 포멧 확인
C 1 CLIENT                        COMPANY                       CREW NO         
'''

            

a = SEGYReader(r"SB_M2511_03_Test_Header.sgy")
b = (a.load_all_data(a.bin_trace_samples))
