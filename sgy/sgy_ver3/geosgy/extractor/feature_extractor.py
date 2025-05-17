from ..config.format_def import ESSENTIAL_FEATURE

class Feature_Extractor:
    def __init__(self):
        pass

    def test_name(self,b):
        for h in ESSENTIAL_FEATURE:
            feature = {
                h["desc"] : b[b["id"] == h["id"]]["data"],
            }
        print(feature)
'''
ESSENTIAL_FEATURE = np.ndarray([
    (13, "channel"),
    (17, "interval"),
    (21, "samples"),
    (25, "sample_code"),
    (305, "Extention_header")

], dtype=_dtype.REF)
'''