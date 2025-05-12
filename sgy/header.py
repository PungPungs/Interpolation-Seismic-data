'''
[import programming check list]

Extenstion (3505 ~ 3506)
    1st. 3521 ~ 3528 if not 0, it's main (add. chek the tape label)
    if 3505 ~ 3506 == -1 -> trace header is variable

Clearly detect byte order (3297 - 3300)
    1. 0x01020304 (16909060) = big-endian
    2. 0x04030201 (67305985) = little-endian, etc
    3. 0x02010403 (33620995) = 16bit swap
    ---------------------------------------------
    4. 0 = this option is applies to rev 2.1 and below

Extended number of samples per data trace (3289 ~ 3292)
    1. if this data isn't 0 overrides the 3223 ~ 3224 original data

Extended sample interval of original field recording (3281 ~ 3288)
    1. if this data isn't 0 overrides the 3219 ~ 3220 original data

Extended sample interval, IEEE double precision (3273 ~ 3280)
    1. if this data isn't 0 overrides the 3217 ~ 3218 original data

Extended number of samples per data trace. (3269 ~ 3272)
    1. if this data isn't 0 ignore the 3221 ~ 3222 original data

Extended number of auxiliary traces per ensemble (3265 - 3268)
    1. if this data isn't 0 overrides the 3215 ~ 3216 original data

Extended number of data traces per ensemble
    1. if this data isn't 0 ignore the 3213 ~ 3214 original data


IF YOU NEED TO USE THIS CONFIG FILE, MAKE -1 IN THE KEY VALUE (EX. 3201, 3300 ..). PYTHON'S INDEX STARTS FROM 0.    
'''

import numpy as np
from dtype import _dtype
from dataclasses import dataclass
from typing import Literal

@dataclass
class METADATA:
    BYTE_ORDER : Literal["big", "little"] = "big"
    EXTENDED_HEADER : int = 0
    BASE_BYTE : int = 3200
    DATA_TRACE : int = 0
    VER : int = 2

BINARY_HEADER = np.array([
    (1, "Job identification number.", 4, False),
    (5, "Line number. For 3-D poststack data, this will typically contain the in-line number.", 4, False),
    (9, "Reel number.", 4, False),
    (13, "Number of data traces per ensemble. Mandatory for prestack data.", 2, False),
    (15, "Number of auxiliary traces per ensemble. Mandatory for prestack data.", 2, False),
    (17, "Sample interval. µs for time, Hz for frequency, m or ft for depth.", 2, False),
    (19, "Sample interval of original field recording.", 2, False),
    (21, "Number of samples per data trace. (Primary data)", 2, True),
    (23, "Number of samples per data trace for original field recording.", 2, False),
    (25, "Data sample format code.", 2, True),
    (27, "Ensemble fold — The expected number of data traces per trace ensemble", 2, False),
    (29, "Trace sorting code. Type of ensemble sorting.", 2, False),
    (31, "Vertical sum code. N = M-1 sum, M in 2~32767.", 2, False),
    (33, "Sweep frequency at start (Hz).", 2, False),
    (35, "Sweep frequency at end (Hz).", 2, False),
    (37, "Sweep length (ms).", 2, False),
    (39, "Sweep type code.", 2, False),
    (41, "Trace number of sweep channel.", 2, False),
    (43, "Sweep taper length at start (ms).", 2, False),
    (45, "Sweep taper length at end (ms).", 2, False),
    (47, "Taper type.", 2, False),
    (49, "Correlated data traces.", 2, False),
    (51, "Binary gain recovered.", 2, False),
    (53, "Amplitude recovery method.", 2, False),
    (55, "Measurement system. 1=meters, 2=feet", 2, False),
    (57, "Impulse signal polarity.", 2, False),
    (59, "Vibratory polarity code. Signal lag angle classification", 2, False),
    (61, "Extended number of data traces per ensemble. Overrides 3213 ~ 3214 if nonzero", 4, True),
    (65, "Extended number of auxiliary traces per ensemble. Overrides 3215 ~ 3216 if nonzero", 4, True),
    (69, "Extended number of samples per data trace. Overrides 3221 ~ 3222 if nonzero", 4, True),
    (73, "Extended sample interval (IEEE 64-bit float). Overrides 3217~3218 if nonzero", 8, True),
    (81, "Extended original sample interval (IEEE 64-bit float). Overrides 3219~3220", 8, True),
    (89, "Extended number of samples per trace in original recording. Overrides 3223~3224", 4, True),
    (93, "Extended ensemble fold. Overrides 3227~3228 if nonzero", 4, False),
    (97, "Byte order detection constant (16909060 = 0x01020304)", 4, True),
    (301, "Major SEG-Y format revision number (8-bit). 0=SEG-Y 1975", 1, False),
    (302, "Minor SEG-Y format revision number (8-bit).", 1, False),
    (303, "Fixed length trace flag (2-byte)", 2, False),
    (305, "Number of 3200-byte Extended Textual File Headers.", 2, True),
    (307, "Maximum number of additional 240-byte trace headers.", 2, False),
    (309, "Survey type. Sum of bit flags from 3 groups", 2, False),
    (311, "Time basis code.", 2, False),
    (313, "Number of traces in this file or stream (64-bit unsigned).", 8, False),
    (321, "Offset of first trace from start of file/stream (64-bit unsigned). Overrides extended header count if nonzero.", 8, False), # 0, -1 이 아니면 그 수만큼 확장 헤더가 있음
    (329, "Number of 3200-byte trailer stanzas after traces (4-byte signed)", 4, False),
], dtype= _dtype.BASE_HEADER)

STANDARD_BASE_HEADER = np.array([
    (1,  "Trace sequence number within line", 4, False),
    (5,  "Trace sequence number within SEG-Y file", 4, False),
    (9,  "Original field record number", 4, False),
    (13, "Trace number within the original field record", 4, False),
    (17, "Energy source point number", 4, False),
    (21, "Ensemble number (i.e. CDP, CMP, CRP, etc.)", 4, False),
    (25, "Trace number within the ensemble", 4, False),
    (29, "Trace identification code", 2, False),   # 코드 참조 가능
    (31, "Number of vertically summed traces yielding this trace", 2, False),   # 상수 맵 있을 가능성
    (33, "Number of horizontally stacked traces yielding this trace", 2, False),
    (35, "Data use", 2, False),
    (37, "Distance from center of the source point to the center of the receiver group ", 4, False),
    (41, "Elevation of receiver group", 4, False),
    (45, "Surface elevation at source location", 4, False),
    (49, "Source depth below surface", 4, False),
    (53, "Seismic Datum elevation at receiver group", 2, False),
    (57, "Seismic Datum elevation at source", 4, False),
    (61, "Water column height at source location", 4, False),
    (65, "Water column height at receiver group location", 4, False),
    (69, "Scalar to be applied to all elevations and depths specified in Standard Trace Header bytes 41~68 to give the real value", 2, False),
    (71, "Scalar to be applied to all coordinates specified in Standard Trace Header bytes 73~88 and to bytes Trace Header 181~188 to give the real value", 2, False),
    (73, "Source coordinate - X", 4, False),
    (77, "Source coordinate - Y", 4, False),
    (81, "Group coordinate - X", 4, False),
    (85, "Group coordinate - Y", 4, False),
    (89, "Coordinate units", 2, False),
    (91, "Weathering velocity", 2, False),
    (93, "Subweathering velocity", 2, False),
    (95, "Uphole time at source in milliseconds", 2, False),
    (97, "Uphole time at group in milliseconds", 2, False),
    (99, "Source static correction in milliseconds", 2, False),
    (101, "Group static correction in milliseconds", 2, False),
    (103, "Total static applied in milliseconds", 2, False),
    (105, "Lag time A — Time in milliseconds between end of 240-byte trace identification header and time break", 2, False),
    (107, "Lag Time B — Time in milliseconds between time break and the initiation time of the energy source", 2, False),
    (109, "Delay recording time", 2, False),
    (111, "Mute time — Start time in milliseconds", 2, False),
    (113, "Mute time — End time in milliseconds", 2, False),
    (115, "Number of samples in this trace", 2, False),
    (117, "Sample interval for this trace", 2, False),
    (119, "Gain type of field instruments", 2, False),
    (121, "Instrument gain constant (dB)", 2, False),
    (123, "Instrument early or initial gain (dB)", 2, False),
    (125, "Correlated", 2, False),
    (127, "Sweep frequency at start (Hz)", 2, False),
    (129, "Sweep frequency at end (Hz)", 2, False),
    (131, "Sweep length in milliseconds", 2, False),
    (133, "Sweep type", 2, False),
    (135, "Sweep trace taper length at start in milliseconds", 2, False),
    (137, "Sweep trace taper length at end in milliseconds", 2, False),
    (139, "Taper type", 2, False),
    (141, "Alias filter frequency (Hz), if used", 2, False),
    (143, "Alias filter slope (dB/octave)", 2, False),
    (145, "Notch filter frequency (Hz), if used", 2, False),
    (147, "Notch filter slope (dB/octave)", 2, False),
    (149, "Low-cut frequency (Hz), if used", 2, False),
    (151, "High-cut frequency (Hz), if used", 2, False),
    (153, "Low-cut slope (dB/octave)", 2, False),
    (155, "High-cut slope (dB/octave)", 2, False),
    (157, "Year data recorded", 2, False),
    (159, "Day of year", 2, False),
    (161, "Hour of day (24-hour clock)", 2, False),
    (163, "Minute of hour", 2, False),
    (165, "Second of minute", 2, False),
    (167, "Time basis code", 2, False),
    (169, "Trace weighting factor", 2, False),
    (171, "Geophone group number of roll switch position one", 2, False),
    (173, "Geophone group number of trace number one within original field record", 2, False),
    (175, "Geophone group number of last trace within original field record", 2, False),
    (177, "Gap size", 2, False),
    (179, "Over travel associated with taper at beginning or end of line", 2, False),
    (181, "X coordinate of ensemble (CDP) position of this trace ", 2, False),
    (185, "Y coordinate of ensemble (CDP) position of this trace", 4, False),
    (189, "For 3-D poststack data, this field should be used for the in-line number", 4, False),
    (193, "For 3-D poststack data", 4, False),
    (197, "Shotpoint number", 4, False),
    (201, "Scalar to be applied to the shotpoint number in Standard Trace Header bytes 197~200 to give the real value", 2, False),
    (203, "Trace value measurement unit", 2, False),
    (205, "Transduction Constant", 8, False),
    (211, "Transduction Unit", 2, False),
    (213, "Device/Trace Identifier ", 2, False),
    (215, "Scalar to be applied to times specified in Trace Header bytes 95~114 to give the true time value in milliseconds", 2, False),
    (217, "Source Type/Orientation", 2, False),
    (219, "Source Energy Direction with respect to the source orientation", 2, False),
    (225, "Source Measurement", 6, False),
    (231, "Source Measurement Unit", 2, False),
    (233, "Either binary zeros or the eight-character trace header name “SEG00000”. May be ASCII or EBCDIC text.", 8, False),
], dtype =  _dtype.BASE_HEADER)

SAMPLING_CODE = np.array([
    (1,  "f4", 4),
    (2,  "i4", 4),
    (3,  "i2", 2),
    # (4,  "4-byte fixed-point with gain (obsolete)", 4),
    (5,  "f4", 4),
    (6,  "f8", 8),
    (7,  "i3", 3),
    (8,  "i2", 1),
    (9,  "i8", 8),
    (10, "u4", 4),
    (11, "u2", 2),
    (12, "u8", 8),
    (15, "u3", 3),
    (16, "u1",  1),
], dtype = _dtype.FORMAT_CODE)


CONDITION = np.array([
    (61, 13), #override
    (65, 15), #override
    (69, 21), #override
    (73, 17), #override
    (81, 19), #override
    (89, 23), #override
    # (69, 21), #override
    # (73, 17), #override
    # {"id" , 3297, "data" , 0, "ref_id" , 3223}, #edian
], dtype = _dtype.COND)