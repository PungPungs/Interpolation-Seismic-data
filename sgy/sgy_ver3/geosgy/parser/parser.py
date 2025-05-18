import re
import numpy as np
from ..config.format_def import BINARY_HEADER, TRACE_HEADER
from ..config.dtype import _dtype
from typing import Literal
import pandas as pd

REGULAR = r"(?=C\s?\d?\d)"

class Parser:
    def __init__(self):
        self.decode : str = ""

    def parsed_trace(self, trace, n):
        length = 240 + (4 * n)
        b = np.frombuffer(trace,dtype=np.uint8).reshape((-1,length))
        th, sp = b[:,:240], b[:,240:]
        raw = {
            "trace_header" : self.__parse_header(th.tobytes(),'trace'),
            "samples" : np.frombuffer(sp.tobytes(),dtype=">f4")
        }
        return raw.items()

    def parsed_headers(self, headers : np.ndarray) -> np.ndarray:
        try:
            text, self.decode = headers[:3200].tobytes().decode("ascii"), "ascii"
        except UnicodeDecodeError:
            text, self.decode = headers[:3200].tobytes().decode("cp500"), "cp500"
        binary = headers[3200:]
        raw = {
            "textual" : re.split(REGULAR,text),
            "binary" : self.__parse_header(binary, kind="binary")
        }
        return raw
    

    ### 헤더 전용
    def __parse_header(self, b : bytes, kind : Literal["binary", "trace"]):
        raw = []
        if kind == "binary":
            header_df = BINARY_HEADER
        else:
            header_df = TRACE_HEADER
        for h in header_df:
            start = h["id"] - 1
            length = h["len"]
            temp = int.from_bytes(b[start : start + length],"big",signed=h["signed"])
            raw.append((
                h["id"],
                h["desc"],
                temp
            ))
        return np.array(raw, dtype=_dtype.BASE_DATA)