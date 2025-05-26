from ..config.format_def import ESSENTIAL_FEATURE

class Feature_Extractor:

    def __init__(self):
        pass

    def from_header(self, header):
        raw = []
        for row in ESSENTIAL_FEATURE:
            raw.append((header[header["id"] == row["id"]]["data"][0]))
        return raw
            