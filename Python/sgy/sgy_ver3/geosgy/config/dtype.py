import numpy as np

class _dtype:
    HEADER = np.dtype([
        ("id", np.uint16),
        ("desc", "U100"),
        ("len",">i4"),
        ("signed", np.bool)
    ])

    FORMAT_CODE = np.dtype([
        ("code", np.uint16),
        ("format", "U20"),
        ("byte",np.uint8),
        ("signed", np.bool)
    ])

    REF = np.dtype(
        [
            ("id", np.uint16),
            ("desc", "U20")
        ]
    )

    BASE_DATA = np.dtype([
        ("id", np.uint16),
        ("desc", "U100"),
        ("data", ">i8"),
    ])

