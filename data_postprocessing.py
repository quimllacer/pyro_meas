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

def analyze(df, electrode_area, points_p_period = 10, freq = 0.01, window = 51 ):
    print("analyzing data...")

    df = df[["time", "current", "ext_temp"]]

    #SAMPLE to reduce file size ########################################
    experiment_time = df["time"].iloc[-1]
    sampling_rate = experiment_time/len(df["time"])
    periods = experiment_time/(1/freq)
    sample_size = periods * points_p_period
    ratio = int(len(df["time"])/sample_size)
    df = df.iloc[::ratio, :]

    t = np.array(df["time"])
    A = df["ext_temp"]
    B = df["current"]

    #FUNCTIONS #########################################################
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

    analyzed_data = []
    for i in range(len(A)):
        margin = int((window-1)/2)
        assert(window % 2 == 1)
        if margin <= i < len(A)-margin:
            tim = t[i-margin:i+margin].copy()
            Ax = A[i-margin:i+margin].copy()
            Bx = B[i-margin:i+margin].copy()

            ti = t[i]
            temp = np.array(A)[i]
            temp_amplitude = abs(sine(Ax, tim))
            T_amp = np.mean(temp_amplitude)
            current = np.array(B)[i]
            current_amplitude = abs(sine(Bx, tim))

            Ax -= Ax.mean(); Ax /= Ax.std(); Ax = detrend(Ax)
            Bx -= Bx.mean(); Bx /= Bx.std(); Bx = detrend(Bx)

            phase = hil(Ax, Bx)
            frequency = 0.01
            # T_amp = 1
            p_coeff = (np.sin(math.radians(phase))*current_amplitude) / (electrode_area* 2*np.pi*frequency*T_amp)
            analyzed_data.append([ti, temp, current, phase, current_amplitude, p_coeff, temp_amplitude])

    out = pd.DataFrame(analyzed_data, columns = ["time", "temperature", "current", "phase", "amplitude", "p_coeff", "temp_amplitude"])
    out["current"] = out["current"]*1e9
    out["amplitude"] = out["amplitude"]*1e9
    out["p_coeff"] = out["p_coeff"]*1e6
    
    fig, axs = plt.subplots(2, figsize=(10,4), sharex=True, sharey=False)
    #fig.suptitle(file_name)
    ax0, ax1, ax2, ax3 = axs[0], axs[0].twinx(), axs[1], axs[1].twinx()
    ax0.plot(out["time"], out["temperature"], color = "blue")
    ax1.plot(out["time"], out["current"], color = "red")
    ax2.plot(out["time"], out["phase"], color = "black")
    ax3.plot(out["time"], out["p_coeff"], color = "green")
    #ax4.plot(out["time"], out["amplitude"], color = "pink")
    ax0.set_yticks([20, 40, 60, 80, 100, 120, 140])
    ax1.set_yticks(np.linspace(-20, 20, 9))
    ax2.set_yticks(np.linspace(-180, 180, 9))
    ax3.set_yticks(np.linspace(-100, 100, 9))
    ax0.set_ylabel('Temperature (°C)')
    ax1.set_ylabel('Current (nA)')
    ax2.set_ylabel('Phase shift (°)')
    ax3.set_ylabel('p ($\mathregular{µC K^{-1} m^{-2}}$)')
    # plt.show()

    return out, fig









