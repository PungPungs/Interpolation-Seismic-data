import mmap
from typing import Literal
from ..parser.parser import Parser


byte_addr = {
    "text" : [0,3200],
    "binary" : [3200, 3600],
}

class Reader:
    def __init__(self, file_path : str):
        self.parser = Parser()
        with open(file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)

    def read_arrange(self, start : int, length : int) -> bytes:
        self.mm.seek(start)
        return self.mm.read(length)


    def read_default(self) -> bytes:
        text = byte_addr.get("text")
        binary = byte_addr.get("binary")
        t = self.read_arrange(*text)
        b = self.read_arrange(*binary)
        return t,b

    def __del__(self) -> None:
        self.mm.close()