'''
S : 부호 1bit
E : 지수 8bit
F : 가수 소수 부분 (23비트)

if e = 255 & f != 0..v = NaN : Not-a-Number (see Note 1)
if e = 255 & f = 0. .v = (-1)^s x inf : Overflow
if 0 < e < 255. . . . v = (-1)s x 2e-127 x (1.f) : Normalized
if e = 0 & f ¹  0. . . .v = (-1)s x 2e-126 x (0.f) : Denormalized 
if e = 0 & f = 0. . . .v = (-1)s x 0 : ± zero
    where  e = binary value of all C's (exponent), f = binary value of all Q's (fraction)
'''
import numpy as np
import datetime
from typing import Literal
a = b'\x7F\xC0\x00\x00'



def ieee_754_4byte(b: bytes, bytes_order : Literal['>','<']) -> np.float32:
    if not isinstance(b, (bytes, bytearray)) or len(b) != 4:
        raise ValueError("Input must be exactly 4 bytes")
    return np.frombuffer(b, dtype= (bytes_order + 'f4'))



def ieee_754_8byte(b: bytes, bytes_order : Literal['>','<']) -> np.float32:
    ''' > -> big endian, < -> little endian'''
    if not isinstance(b, (bytes, bytearray)) or len(b) != 4:
        raise ValueError("Input must be exactly 4 bytes")
    return np.frombuffer(b, dtype= (bytes_order + 'f8'))




