# PID for the for the thermoelectric heater-cooler (peltier element)
import sys
import time
import math
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.signal import hilbert
from datetime import datetime
from general_functions import new_datefolder
from scipy.signal import correlate, correlation_lags, detrend

file = r"/Users/joaquinllacerwintle/OneDrive - ETH Zurich/pyroelectric measurements/data/20210903/01h27m58s_test_poled_pvdf_inverted_pol_20000s_TEMP_1a0.01f0.002s80o.xlsx"
df = pd.read_excel(file, engine = "openpyxl")[["time", "current", "ext_temp"]] # Skip intital rows

# df["current"] = df["current"].rolling(30, center = True).mean()
# df["ext_temp"] = df["ext_temp"].rolling(3, center = True).mean()
df = df.dropna()

t = np.array(df["time"])
A = df["ext_temp"]
B = df["current"]

timedeltas = [t[i-1] - t[i] for i in range(1, len(t))]
sampling_rate = abs(sum(timedeltas))/len(timedeltas)
freq = 0.01
window = int(1/(freq*sampling_rate))
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
    guess_phase = 0
    guess_offset = np.mean(A)
    optimize_func = lambda x: (x[0]*np.sin(2*np.pi*freq*t+x[1]) + x[2] - A)
    est_amp, est_phase, est_offset = leastsq(optimize_func, [guess_amp, guess_phase, guess_offset])[0]
    data_fit = est_amp*np.sin(2*np.pi*freq*t+est_phase) + est_offset
    return data_fit



time_phase = []
for i in range(len(A)):
    margin = int((window-1)/2)
    assert(window % 2 == 1)
    if margin <= i < len(A)-margin:
        Ax = A[i-margin:i+margin].copy()
        Bx = B[i-margin:i+margin].copy()

        Ax -= Ax.mean(); Ax /= Ax.std(); Ax = detrend(Ax)
        Bx -= Bx.mean(); Bx /= Bx.std(); Bx = detrend(Bx)

        phase = hil(Ax, Bx)
        ti = t[i]
        time_phase.append([ti, phase])

        # plt.plot(t[i-margin:i+margin], Ax)
        # plt.plot(t[i-margin:i+margin], Bx)
        # plt.ylim([70, 130])
        #plt.ylim([-200E-12, 200E-12])
        plt.show()

out = pd.DataFrame(time_phase, columns = ["time", "phase"])
print(out)
print("Mean phase shift: {}".format(abs(out.phase).mean()))

A -= A.mean(); A /= A.std(); A = detrend(A)
B -= B.mean(); B /= B.std(); B = detrend(B)
# out["phase"] -= out["phase"].mean()

plt.plot(t, A)
plt.plot(t, B)
plt.plot(out["time"], abs(out["phase"]))
# plt.xlim([2000, 5000])
plt.ylim([-180, 180])
plt.show()









