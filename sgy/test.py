import numpy as np
from collections import deque
from header import BINARY_HEADER,STANDARD_BASE_HEADER
import mmap
import pandas as pd
import struct


class META_DATA:
    fmt = {
        1 : 'b',
        2 : 'h',
        4 : 'i',
        6 : 'ii',
        8 : 'd',
    }
    def __init__(self, name):
        self.name = name
        with open("241115_073433_795565.sgy","rb") as f:
            self.mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        self.mm.seek(3200)
        b = self.mm.read(400)
        rows = self.load_to_binary_(b)
        print(pd.DataFrame(rows)["data"])
        self.mm.seek(3600)
        b = self.mm.read(240)
        rows = self.load_to_text_(b)
        print(pd.DataFrame(rows))

    
    def load_to_binary_(self, b : bytes):
        _row = []
        for _header in BINARY_HEADER:
            start = _header["id"]
            fmt = self.fmt.get(_header["len"])
            _row.append({
                "id" : start,
                "desc" : _header["desc"],
                "data" : struct.unpack_from(f">{fmt}",b,start-1),
            })
        return _row

    
    def load_to_text_(self, b : bytes):
        _row = []
        for _header in STANDARD_BASE_HEADER:
            start = _header["id"]
            fmt = self.fmt.get(_header["len"])
            _row.append({
                "id" : start,
                "desc" : _header["desc"],
                "data" : struct.unpack_from(f">{fmt}",b,start-1),
            })
        return _row


    SEGY_META_DATA = {
        # default        
        "Binary_header_length" : int,
        "Std_trace_header_length" : int,
        "VER" : int,

        # read and refresh
        "Encoding_type" : str, # error_check
        "Num_of_trace" : int, # binary 13 ~ 14
        "Num_of_Sample" : int, # binary 21 ~ 22
        "Format_type" : str, # binary 25 ~ 26
        "Endian" : str, # binary 97 ~ 100
        "Num_of_Extended" : int, # binary 305 ~ 306,
    }

    SEGY_HEADER_DATA = {
        "Text_Header" : np.ndarray,
        "Binary_Header" : np.ndarray,
        "Std_Trace_Header" : np.ndarray,
    }


line_1 = META_DATA("line_1")
