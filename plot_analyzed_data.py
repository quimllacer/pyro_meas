import sys
import time
import math
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq, curve_fit
from scipy.signal import hilbert
from datetime import datetime
from general_functions import new_datefolder
from scipy.signal import correlate, correlation_lags, detrend
import ntpath
import seaborn as sns
sns.set_style("ticks")

file_name = "/Users/joaquinllacerwintle/OneDrive - ETH Zurich/data/20211023/21h48m52s_52500s_poled-pvdf-testANALYZED.xlsx"
temp_min = 25
temp_max = 125
curr_min = -15
curr_max = 15
coef_min = -200
coef_max = 200


out = pd.read_excel('{}'.format(file_name), engine = "openpyxl")

print(out)


fig, axs = plt.subplots(2, figsize=(10,4), sharex=True, sharey=False)
#fig.suptitle(file_name)
ax0, ax1, ax2, ax3 = axs[0], axs[0].twinx(), axs[1], axs[1].twinx()
ax0.plot(out["time"], out["temperature"], color = "blue")
ax1.plot(out["time"], out["current"]*1e9, color = "red")
ax2.plot(out["time"], out["phase"], color = "black")
ax3.plot(out["time"], out["p_coeff"]*1e6, color = "green")
#ax4.plot(out["time"], out["amplitude"], color = "pink")
ax0.set_yticks(np.linspace(temp_min, temp_max, 9))
ax1.set_yticks(np.linspace(curr_min, curr_max, 9))
ax2.set_yticks(np.linspace(-180, 180, 9))
ax3.set_yticks(np.linspace(coef_min, coef_max, 9))
ax0.set_ylabel('Temperature (°C)', weight = "bold", fontsize = 12)
ax1.set_ylabel('Current (nA)', weight = "bold", fontsize = 12)
ax2.set_ylabel('Phase shift (°)', weight = "bold", fontsize = 12)
ax3.set_ylabel('p ($\mathregular{µC K^{-1} m^{-2}}$)', weight = "bold", fontsize = 12)
ax2.set_xlabel('Time (s)', weight = "bold", fontsize = 12)
ax0.yaxis.label.set_color('blue')
ax1.yaxis.label.set_color('red')
ax2.yaxis.label.set_color('black')
ax3.yaxis.label.set_color('green')
plt.show()