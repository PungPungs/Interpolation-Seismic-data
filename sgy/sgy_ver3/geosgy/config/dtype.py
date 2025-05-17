import numpy as np

class _dtype:
    BASE_HEADER = np.dtype([
        ("id", np.uint16),
        ("desc", "U100"),
        ("len", np.uint16),
    ])

    FORMAT_CODE = np.dtype([
        ("code", np.uint16),
        ("format", "U20"),
        ("byte",np.uint8)
    ])

    REF = np.dtype(
        [
            ("id", np.uint16),
            ("desc", "U20")
        ]
    )


