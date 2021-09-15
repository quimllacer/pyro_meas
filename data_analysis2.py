# PID for the for the thermoelectric heater-cooler (peltier element)
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

file = r"/Users/joaquinllacerwintle/OneDrive - ETH Zurich/data/important data/Corona poled PVDF PtoN second cycle.xlsx"
df = pd.read_excel(file, engine = "openpyxl")[["time", "current", "ext_temp"]] # Skip intital rows

df = df.iloc[::10, :] # Take 1 out of nth rows
# df["current"] = df["current"].rolling(30, center = True).mean()
# df["ext_temp"] = df["ext_temp"].rolling(3, center = True).mean()
df = df.dropna()

t = np.array(df["time"])
A = df["ext_temp"]
B = df["current"]

timedeltas = [t[i-1] - t[i] for i in range(1, len(t))]
sampling_rate = abs(sum(timedeltas))/len(timedeltas)
freq = 0.01
window = int(2/(freq*sampling_rate))
if window % 2 == 0:
    window += 1
print(window)

def hil(A, B):
    A_h = hilbert(A)
    B_h = hilbert(B)
    c = np.inner( A_h, np.conj(B_h) ) / math.sqrt( np.inner(A_h,np.conj(A_h)) * np.inner(B_h,np.conj(B_h)) )
    phase_rad = np.angle(c)
    return math.degrees(phase_rad)

def xcorr(A, B):
    phase = correlate(A, B)
    lags = correlation_lags(len(A), len(B))
    lag_indx = list(phase).index(max(phase))
    lag = lags[lag_indx]
    phase_deg = math.degrees(lag*sampling_rate*(2*np.pi*freq))
    return phase_deg

def sine(A, t):
    guess_amp = 1
    guess_freq = 0.01
    guess_slope = 0
    guess_offset = np.mean(A)
    optimize_func = lambda x: (x[0]*np.sin(2*np.pi*x[1]*t) + x[2] + t*x[3] - A)
    est_amp, est_freq, est_offset, est_slope = leastsq(optimize_func, [guess_amp, guess_freq, guess_offset, guess_slope])[0]
    data_fit = est_amp*np.sin(2*np.pi*freq*t) + est_offset
    return est_amp

time_phase = []
for i in range(len(A)):
    margin = int((window-1)/2)
    assert(window % 2 == 1)
    if margin <= i < len(A)-margin:
        tim = t[i-margin:i+margin].copy()
        Ax = A[i-margin:i+margin].copy()
        Bx = B[i-margin:i+margin].copy()

        current_amplitude = abs(sine(Bx, tim))

        Ax -= Ax.mean(); Ax /= Ax.std(); Ax = detrend(Ax)
        Bx -= Bx.mean(); Bx /= Bx.std(); Bx = detrend(Bx)

        phase = hil(Ax, Bx)
        electrode_area = 240e-6
        frequency = 0.01
        T_amp = 1
        p_coeff = (np.sin(math.radians(phase))*current_amplitude) / (electrode_area* 2*np.pi*frequency*T_amp)
        ti = t[i]
        time_phase.append([ti, phase, current_amplitude, p_coeff])

        # plt.plot(t[i-margin:i+margin], Ax)
        # plt.plot(t[i-margin:i+margin], Bx)
        # plt.ylim([70, 130])
        #plt.ylim([-200E-12, 200E-12])
        plt.show()

out = pd.DataFrame(time_phase, columns = ["time", "phase", "amplitude", "p_coeff"])
out = out.iloc[::50, :] # Take 1 out of nth rows
print(out)
out.to_excel("processed_data.xlsx")
print("Mean phase shift: {}".format(abs(out.phase).mean()))

fig, axs = plt.subplots(5, sharex=True, sharey=False)
fig.suptitle('Plot name')
axs[0].plot(t, A)
axs[1].plot(t, B)
axs[2].plot(out["time"], out["phase"])
axs[3].plot(out["time"], out["amplitude"])
axs[4].plot(out["time"], out["p_coeff"])
axs[2].set_yticks([-180, -90, 0, 90, 180])
plt.show()









