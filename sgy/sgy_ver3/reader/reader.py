import mmap

class Reader:
    def __init__(self, file_path : str):
        with open(file_path, "rb") as f:
            self.mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)

    def read_arrange(self, start : int, length : int) -> bytes:
        self.mm.seek(start)
        return self.mm.read(length)

    def __del__(self) -> None:
        self.mm.close()