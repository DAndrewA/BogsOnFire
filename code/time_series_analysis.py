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
data = pd.read_csv(r'C:\Users\s1834371\Documents\PhD\SENSE_training\Bogs\code\ndvi_ndwi_data_v2.csv')
data = data.dropna()
date = pd.to_datetime(data['date'], dayfirst=True, format='%d/%m/%Y').values
print(data)
ndvi = data['NDVI'].values
ndwi = data['NDWI'].values

#-----------FFT----------------------------
fft = np.fft.fft(ndwi)
fft_abs = np.abs(fft)

cutoff = 10
fft[cutoff:] = 0


fig = plt.figure()
spec = gridspec.GridSpec(ncols=1, nrows=1)
#-----------------------------ax1----------------------------------------
ax1 = fig.add_subplot(spec[0,:])
ax1.plot(date, fft, label='fft', color='limegreen')
ax1.plot(date, fft_abs, label='fft_abs', color='b')

#---formatting dates--------------------------------------
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax1.tick_params(axis='x', which='major', rotation=90)

ax1.legend()
ax1.set_xlim(date[0], date[-1])

figure_filename = 'ndvi_ndwi_figure.png'

width = 6.88 + 3
height = width/1.618 - 2


fig.set_size_inches(width, height)
fig.savefig(figure_filename, dpi=300,  bbox_inches='tight')
plt.show()