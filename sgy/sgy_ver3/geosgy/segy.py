from .reader.reader import Reader
from .parser.parser import Parser
from .extractor.feature_extractor import Feature_Extractor
from .reader.reader import Reader
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class SegyInfo:
    textual_header : list = None
    binary_header : np.ndarray = None
    trace_header : np.ndarray = None
    samle : np.ndarray = None
    format_code : np.ndarray = None
    channel : int = None
    num_of_sample : int = None
    interval : int = None

class SEGY:
    def __init__(self, file_path : str):
        self.file_path = file_path
        self.reader = Reader(file_path)
        self.parser = Parser()
        self.segy_info = SegyInfo()
        self.feature_extracrtor = Feature_Extractor()


    def load(self):
        bin_header = self.reader.read_header()
        headers = self.parser.parsed_headers(bin_header)
        feature = self.feature_extracrtor.from_header(headers.get("binary"))
        self.channel = feature[0]
        self.interval = feature[1]
        self.num_of_sample = feature[2]
        self.fomat_code = feature[3]
        self.extended = feature[4]
        td = self.reader.read_trace()
        print(self.parser.parsed_trace(td, self.num_of_sample))

        

        

    def modify(self):
        pass