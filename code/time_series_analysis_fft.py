import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates
import matplotlib as mpl
tick_fontsize = 8
label_fontsize = 9 
title_fontsize = 10
mpl.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.linewidth'] = 1.2
plt.rc('xtick', labelsize=tick_fontsize, direction='in')
plt.rc('ytick', labelsize=tick_fontsize, direction='in')
plt.rc('axes', labelsize=label_fontsize)
plt.rc('axes', titlesize=title_fontsize)
plt.rc('legend', fontsize=tick_fontsize)    # legend fontsize
plt.rc('figure', titlesize=title_fontsize)  # fontsize of the figure title
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams["xtick.major.size"] = 8
plt.rcParams["ytick.major.size"] = 8
plt.rcParams["xtick.minor.size"] = 4
plt.rcParams["ytick.minor.size"] = 4

#--------------import data----------------------------------
data = pd.read_csv(r'C:\Users\s1834371\Documents\PhD\SENSE_training\Bogs\code\NDVI_NDWI_data_v2.csv')
data = data.dropna()
date_dt = pd.to_datetime(data['date'], dayfirst=True, format='%d/%m/%Y')
date = date_dt.values
ndvi = data['NDVI'].values
ndwi = data['NDWI'].values

data_wider = pd.read_csv(r'C:\Users\s1834371\Documents\PhD\SENSE_training\Bogs\code\NDVI_NDWI_wide_data_v2.csv')
data_wider = data_wider.dropna()
ndvi_wider = data_wider['NDVI'].values
ndwi_wider = data_wider['NDWI'].values

#-----------FFT----------------------------
fft = np.fft.fft(ndwi_wider)
fft_abs = np.abs(fft)

cutoff = 12
fft[cutoff:] = 0
new_ndwi = np.fft.ifft(fft)

anomaly = (ndwi - new_ndwi)

#===================================creating figure=======================================================
fig = plt.figure()
spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[1.5,1], hspace=0.1)
#-----------------------------ax1----------------------------------------
ax1 = fig.add_subplot(spec[0])
ax1.plot(date, new_ndwi, label='Background NDWI', color='k', linestyle='--')
ax1.plot(date, ndwi, label='NDWI burnt', color='b')
ax1.plot(date, ndvi, label='NDVI burnt', color='limegreen', zorder=-1)

ax1.vlines(x=pd.to_datetime('2019-05-01'), ymin=-1, ymax=1, colors='r', zorder=-4)
ax1.text(x=pd.to_datetime('2019-05-09'), y=0.75, s='Wildfire (16th May 2019)', color='red')
ax1.set_title('NWDI and NDVI')
#---formatting dates--------------------------------------
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.set_xticklabels([])
ax1.legend()
ax1.set_xlim(date[0], date[-1])
ax1.set_ylim(-0.3,0.9)
ax1.set_ylabel('Index Value')
#-------------------------------ax2-------------------------------------------
ax2 = fig.add_subplot(spec[1])

ax2.bar(date_dt, anomaly, width=30, color='grey', edgecolor='k')
ax2.set_ylim(-0.6, 0.6)
ax2.set_xticklabels([])
ax2.set_ylabel('NDWI Anomaly')

#---formatting dates--------------------------------------
ax2.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y %b'))
ax2.tick_params(axis='x', which='both', rotation=90)
ax2.set_xlim(date[0], date[-1])

ax2.vlines(x=pd.to_datetime('2019-05-01'), ymin=-1, ymax=1, colors='r', zorder=-4)

#----------saving figure---------------------
figure_filename = r'code\ndvi_ndwi_figure.png'
width = 6.88 + 4
height = width/1.618 - 2

fig.set_size_inches(width, height)
fig.savefig(figure_filename, dpi=300,  bbox_inches='tight')
plt.show()

