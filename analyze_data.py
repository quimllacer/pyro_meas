import numpy as np
import pandas as pd
import csv

from data_analysis import analyze


file_name = "/home/pi/git_repos/data/20211210/07h29m37s_22500s_50micron_drop."

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

analyzed_data, figure = analyze(df, points_p_period = 10, freq = 0.01, window = 51)
analyzed_data.to_excel('{}.xlsx'.format(file_name + "ANALYZED"))
figure.savefig('{}.png'.format(file_name + "ANALYZED"))