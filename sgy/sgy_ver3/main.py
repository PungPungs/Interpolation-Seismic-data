from geosgy import SEGY,Reader, Parser

sgy = SEGY("C:\DEV\Code\Python\Interpolation-Seismic-data\sgy\SB_M2511_03_Test_Header.sgy")
reader = Reader(r"C:\DEV\Code\Python\Interpolation-Seismic-data\sgy\241115_073433_795565.sgy")
parser = Parser()
b_info = reader.read_default()
