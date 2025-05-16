import numpy as np

class Parser:
    def __init__(self):
        pass

    def binary_parser(self):
        pass

    def split_header_sample(self, b : bytes, trace_length : int) -> np.ndarray:
        temp = np.frombuffer(b,"uint8").reshape(-1,trace_length)
        header, sample = temp[:240], temp[240:]
        return header, sample
        
