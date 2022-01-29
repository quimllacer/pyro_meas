import numpy as np
import pandas as pd
import csv

from data_postprocessing import analyze


file_name = "/Users/joaquinllacerwintle/OneDrive - ETH Zurich/data/20220128 (1)/16h03m35s_20000s_joaquim_circular100_poledwithoutelectrodes"
# Parameters
electrode_area = 240e-6 # Area of the measuring electrode in m2.

df = pd.read_csv('{}.csv'.format(file_name), names = ["current",
                                   "time",
                                   "ext_temp",
                                   "int_temp",
                                   "new_target_temp",
                                   "pid_out_volt",
                                   "pelt_volt",
                                   "pelt_curr",
                                   "vsource"])
df = df[["time",
         "current",
         "int_temp",
         "ext_temp",
         "new_target_temp",
         "pid_out_volt",
         "pelt_volt",
         "pelt_curr",
         "vsource"]]

print(df.tail(20))

analyzed_data, figure = analyze(df = df, electrode_area = electrode_area, points_p_period = 10, freq = 0.01, window = 51)
analyzed_data.to_excel('{}.xlsx'.format(file_name + "REANALYZED"))
figure.savefig('{}.png'.format(file_name + "REANALYZED"))