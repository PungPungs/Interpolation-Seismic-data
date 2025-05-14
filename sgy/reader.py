import numpy as np
import mmap
import pandas as pd
import struct
from header import BINARY_HEADER, STANDARD_BASE_HEADER
from typing import Literal, Tuple, List

class SEGYReader:
    fmt : Tuple[int,str] = {
        1: 'b',
        2: 'h',
        4: 'i',
        6: 'hi',
        8: 'q',
    }

    read_header : Tuple[str,List] = {
        "text": [0, 3200],
        "binary": [3200, 400],
        "trace": [3600, 240],
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.text_header = ""
        self.binary_header = pd.DataFrame()
        self.trace_header = pd.DataFrame()
        self.encoding = "ascii"

        with open(self.file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        
        self._read_headers()
        self.extract_features()
        self.samples = pd.DataFrame(self.read_trace())

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
            fmt = self.fmt.get(h["len"])
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
        self.format = self.binary_header[self.binary_header["id"] == 25]["data"].item()
        
    def read_trace(self):
        self.total_size = self.mm.size()
        step = 240 + self.num_of_sample * 4
        trace_data_size = self.total_size - 3600

        if step <= 0:
            return None

        if trace_data_size % step != 0:
            raise ValueError("트레이스 길이가 맞지 않습니다.")
        self.channel = trace_data_size // step

        self.mm.seek(3600)
        b = self.mm.read(trace_data_size)
        self.trace_header, self.samples = self.split_trace_data(b)
        self.all_parse_header(self.trace_header)
    
    # numpy 배열로 받고 필요할 때 마다 라인별로 읽기
    def split_trace_data(self, b : bytes) -> Tuple[np.ndarray, np.ndarray]:
        step = 240 + self.num_of_sample * 4
        raw = np.frombuffer(b, dtype=np.uint8).reshape((-1, step))
        header = raw[:, :240]
        sample =  raw[:, 240:]
        return header, sample
        

    def all_parse_sample(self,b : np.ndarray):
        return np.frombuffer(b.tobytes(), dtype=">f4").reshape((-1, self.num_of_sample))

### 작업 전
    def all_parse_header(self,b : np.ndarray):
        row = []
        for _b in b:
            row.append(self._parse_header(_b.tobytes(), 'trace'))

            
a = SEGYReader(r"SB_M2511_03_Test_Header.sgy")