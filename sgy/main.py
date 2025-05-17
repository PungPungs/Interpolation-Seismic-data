from sgy_ver3.geosgy import Reader,Parser,Feature_Extractor


reader = Reader(r"C:\dev\Code\Interpolation-Seismic-data\sgy\241115_073433_795565.sgy")
text, header = reader.read_default()
parser = Parser(text, header)
print(parser.headers)
