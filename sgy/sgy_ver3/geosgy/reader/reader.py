import mmap
import numpy as np

TRACE_START = 3600

class Reader:

    def __init__(self, file_path):
        with open(file_path, "rb") as f:
            self.__mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        self.total = self.__mm.size()

    def __del__(self):
        self.__mm.close()

    def read_header(self) -> np.ndarray[bytes]:
        '''기초 바이니러 헤더 읽음 (0 ~ 3600)'''
        self.__mm.seek(0)
        return np.frombuffer(self.__mm.read(3600), dtype="uint8")
    
    def read_trace(self):
        self.__mm.seek(TRACE_START)
        trace_size = self.total - TRACE_START
        return self.__mm.read(trace_size)

    # def read_header(self):
    #     raw = []
    #     for start, length in self.header_map:
    #         self.mm.seek(start)
    #         raw.append(self.mm.read(length))
    #     return raw