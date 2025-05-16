numpy_dtype_map = {
    "i1":  {"desc": "int8",         "bytes": 1, "signed": True},
    "u1":  {"desc": "uint8",        "bytes": 1, "signed": False},
    "i2":  {"desc": "int16",        "bytes": 2, "signed": True},
    "u2":  {"desc": "uint16",       "bytes": 2, "signed": False},
    "i4":  {"desc": "int32",        "bytes": 4, "signed": True},
    "u4":  {"desc": "uint32",       "bytes": 4, "signed": False},
    "i8":  {"desc": "int64",        "bytes": 8, "signed": True},
    "u8":  {"desc": "uint64",       "bytes": 8, "signed": False},
    "f2":  {"desc": "float16",      "bytes": 2, "signed": True},
    "f4":  {"desc": "float32",      "bytes": 4, "signed": True},
    "f8":  {"desc": "float64",      "bytes": 8, "signed": True},
    "c8":  {"desc": "complex64",    "bytes": 8, "signed": True},   # 2 x float32
    "c16": {"desc": "complex128",   "bytes": 16, "signed": True},  # 2 x float64
}