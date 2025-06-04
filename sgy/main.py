from sgy_ver3.geosgy import SEGY


f = SEGY(r"SB_M2511_03_Test_Header.sgy")
aa  = (f.load())
