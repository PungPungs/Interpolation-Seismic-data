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
        ("format", "U150"),
        ("byte",np.uint8)
    ])

    COND = np.dtype([
        ("id" , np.uint16),
        ("data", np.intc),
        ("ref_id", np.int16) 
    ])
