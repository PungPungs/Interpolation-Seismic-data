from ..config.format_def import ESSENTIAL_FEATURE
from ..config.dtype import _dtype
from typing import Dict, List
import numpy as np
import pandas as pd

class Feature_Extractor:

    def __init__(self):
        pass

    def from_binary_header(self, header : Dict[str,bytes]) -> Dict[str,np.int64]:
        raw = {}
        raw.update()
        for row in ESSENTIAL_FEATURE:
            raw.update({
                row["desc"].item() : header[header["id"] == row["id"]]["data"][0]
                })
        return raw