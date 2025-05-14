from typing import List, Literal, Optional
import pandas as pd
import numpy as np
import mmap
from math import isclose



class Sgy:

    def __init__(self, file_path) -> None:
        # 
        np.set_printoptions(suppress=True)
        with open(file_path, mode="rb") as _f:
            self.mm = mmap.mmap(_f,access=mmap.ACCESS_READ)
    


        

        






if __name__ == "__main__":
    sgy = Sgy(r"241115_073433_795565.sgy")
    sgy.close()