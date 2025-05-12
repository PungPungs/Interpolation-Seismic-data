import numpy as np

class _dtype:
    BASE_HEADER = np.dtype([
        ("id", np.uint16),
        ("desc", "U100"),
        ("len", np.uint8),
        ("ref", np.bool_)
    ])

    FORMAT_CODE = np.dtype([
        ("code", np.uint8),
        ("format", "U20"),
        ("byte",np.uint8)
    ])

    COND = np.dtype([
        ("id" , np.uint16),
        ("ref_id", np.int16) 
    ])
