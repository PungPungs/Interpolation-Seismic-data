from sgy_ver3.geosgy import SEGY


f = SEGY(r"C:\dev\Code\Interpolation-Seismic-data\sgy\241115_073433_795565.sgy")
print(f.load())