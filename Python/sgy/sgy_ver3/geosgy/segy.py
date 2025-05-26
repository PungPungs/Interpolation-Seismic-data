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
    sample : np.ndarray = None
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
        pass
        

        

    def modify(self):
        pass