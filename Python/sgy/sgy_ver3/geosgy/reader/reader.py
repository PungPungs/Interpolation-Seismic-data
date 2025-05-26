import mmap
import numpy as np

TRACE_START = 3600

class Reader:

    def __init__(self, file_path):
        with open(file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        self.total = self.mm.size()

    def __del__(self):
        self.mm.close()

    def read_header(self):
        self.mm.seek(0)
        return np.frombuffer(self.mm.read(3600), dtype="uint8")
    
    def read_trace(self):
        self.mm.seek(TRACE_START)
        trace_size = self.total - TRACE_START
        return self.mm.read(trace_size)

    # def read_header(self):
    #     raw = []
    #     for start, length in self.header_map:
    #         self.mm.seek(start)
    #         raw.append(self.mm.read(length))
    #     return raw