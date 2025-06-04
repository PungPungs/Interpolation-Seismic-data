from .reader.reader import Reader
from .parser.parser import Parser
from .extractor.feature_extractor import Feature_Extractor
from .reader.reader import Reader
from dataclasses import dataclass
import numpy as np
import pandas as pd
import datetime 
@dataclass
class Trace:
    trace_header : np.ndarray = None
    sample : np.ndarray = None



class SEGY:
    def __init__(self, file_path : str):
        self.file_path = file_path
        self.reader = Reader(file_path)
        self.parser = Parser()
        self.trace = Trace()
        self.feature_extracrtor = Feature_Extractor()


    def load(self):
        '''1만개 데이터 기준 소요 시간 : 7초'''
        print(datetime.datetime.now())
        headers = self.parser.parsed_headers(self.reader.read_header())
        feature = self.feature_extracrtor.from_binary_header(headers.get("binary"))
        self.channel, self.interval, self.samples, self.sample_code, self.extend_header = feature.get("channel"), feature.get("interval"), feature.get("samples"), feature.get("sample_code"), feature.get("extend_header"),
        traces = self.reader.read_trace()
        trace_header, trace_sample = self.parser.parsed_trace(traces,self.samples)
        self.trace.trace_header, self.trace.sample = trace_header, trace_sample
        print(self.trace.trace_header)
        print(self.trace.sample)
    
    def get_sample(self):
        print(self.trace.sample.shape)
        return self.trace.sample



        

        

    def modify(self):
        pass