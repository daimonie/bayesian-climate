from matplotlib import pyplot as plt
import pandas as pd
import netCDF4

url='/opt/container/data/dataset.nc'
vname = 'Tx_1211'
station = 0

nc = netCDF4.Dataset(url)
print(nc.dimensions['time'].name)
print(nc.variables['temperature'].long_name)
# h = nc.variables[vname]
# times = nc.variables['time']
# jd = netCDF4.num2date(times[:],times.units)
# hs = pd.Series(h[:,station],index=jd)
