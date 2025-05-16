import re
import numpy as np
from typing import Tuple
from dataclasses import dataclass

# 엔트리포인트 설계를 위한 데이터클래스
@dataclass
class ParsedResult:
    header : np.ndarray = None
    sample : np.ndarray = None
    meta : dict = None

    

class Parser:
    # 읽고 텍스트 및 바이너리 헤더 파싱, 만약 필요한 정보가 없다면 트레이스 데이터 하나 파싱.
    def __init__(self):
        self._trace_data = {}

    def _parser_binary(self, b : bytes, header_df : Tuple) -> np.ndarray:
        return self._parse_header(b,header_df)

    def _split_header_sample(self, b : bytes, trace_length : int) -> None:
        temp = np.frombuffer(b,"uint8").reshape(-1,trace_length)
        header, sample = temp[:240], temp[240:]
        self._trace_data = {"header" : header, "sample" : sample}
        # return ParsedResult(header=header, sample=sample)

    def _parse_trace_headers(self, header_df) -> np.ndarray:
        headers = self._trace_data.get("header")
        if headers is None:
            raise ValueError(f"headers had no data")
        return np.stack(self._parse_header(headers,header_df), axis=0)

    # format 이 필요해~
    def _parse_trace_samples(self) -> np.ndarray:
        samples = self._trace_data.get("sample")
        if samples is None:
            raise ValueError(f"samples had no data")
        return np.frombuffer(samples.tobytes(),dtype=">f4")
    
    def _parse_header(self, b : bytes | np.ndarray, header_df) -> np.ndarray:
        if not isinstance(b,np.ndarray):
            b = np.frombuffer(b, "uint8")          
        raw = []
        for h in header_df:
            start = h["id"] - 1
            size = h["size"]
            fmt = self.fmt.get(size)
            if b.ndim == 2:
                temp = b[:, start : start + size]
            else:
                temp = b[start : start + size]
            raw.append(np.frombuffer(temp.tobytes(),fmt))
        return np.stack(raw, axis=0)
    
    def _parse_text_header(self,b : bytes):
        try:
            t_head = b.decode("ascii")
            encode = "ascii"
        except UnicodeDecodeError:
            t_head = b.decode("cp500")
            encode = "cp500"
        temp = re.split(r"(?=C\s?\d?\d)", t_head)
        return temp


        