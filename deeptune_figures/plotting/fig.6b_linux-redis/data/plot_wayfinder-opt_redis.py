#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    @author: Daniel Oñoro Rubio
    @organization: NEC Europe
    @contact: daniel.onoro@neclab.eu
    @date: Created at 2022-08-16
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

np.random.seed(0)

# Constants
WAYFINDER_DATA_FOLDER = 'linux-redis_sqlite-tl/*.xlsx'
DATA_OUTPUT = './'

N_SAMPLES = 25
N_TRIALS = 10
DEFAULT_VALUE = 58000   # REDIS

# Plot random
########################################################################################################################
# Load data
df = pd.read_excel('../../simulation_data/linux-redis_3_only_OS_single_core.xlsx')
y = np.array(df['throughput'])
best_discovered_sim = []
for i in range(N_TRIALS):
    np.random.shuffle(y)
    # Perform simulation
    sam_y = y[:N_SAMPLES]
    # Get data
    best_over_time = []
    for j in range(1, N_SAMPLES):
        best_over_time.append(np.max(sam_y[:j]))
    # Hold data
    best_discovered_sim.append(np.array(best_over_time))

# Convert into array
best_over_time = np.vstack(best_discovered_sim)

# Compute statistics
avg_best_over_time = best_over_time.mean(axis=0)
std_best_over_time = best_over_time.std(axis=0)
x_time = np.arange(N_SAMPLES-1) + 1

# Plot
lower_bound = avg_best_over_time - std_best_over_time
upper_bound = avg_best_over_time + std_best_over_time

x_time = [150.49, 72.53, 72.56, 65.01, 67.57, 85.04, 72.60, 45.09, 45.03, 45.04, 45.02, 45.00]
m_x_time = np.mean(x_time)  # Nginx
s_x_time = np.std(x_time)  # Nginx
x_time_random = np.cumsum(np.random.normal(m_x_time, s_x_time, size=N_SAMPLES-1))

plt.plot(x_time_random, avg_best_over_time, label='Random')
plt.fill_between(x_time_random, lower_bound, upper_bound, alpha=.3)



# Plot Wayfinder-opt
########################################################################################################################
results_file_list = glob.glob(WAYFINDER_DATA_FOLDER)

best_discovered_sim = []
for results_file in results_file_list:
    # Load data
    df = pd.read_excel(results_file)
    arg_idx = np.argsort(df['perm_id'])
    y = np.array(df['throughput'])
    y = y[arg_idx]

    # Perform simulation
    sam_y = y[:N_SAMPLES]
    # Get data
    best_over_time = []
    for j in range(1, N_SAMPLES):
        best_over_time.append(np.max(sam_y[:j]))
    # Hold data
    best_discovered_sim.append(np.array(best_over_time))

# Convert into array
best_over_time = np.vstack(best_discovered_sim)

# Compute statistics
avg_best_over_time = best_over_time.mean(axis=0)
std_best_over_time = best_over_time.std(axis=0)
x_time = np.arange(N_SAMPLES-1) + 1

# Plot
lower_bound = avg_best_over_time - std_best_over_time
upper_bound = avg_best_over_time + std_best_over_time

mem_time_df = pd.read_csv(DATA_OUTPUT + 'n_samples-mem-time_1.csv')
x_time = x_time_random + mem_time_df['time'][:N_SAMPLES-1]

plt.plot(x_time, avg_best_over_time, label='DeepTune')
plt.fill_between(x_time, lower_bound, upper_bound, alpha=.3)

# Plot default value
#########################################################
plt.hlines(DEFAULT_VALUE, xmin=x_time[0], xmax=x_time[N_SAMPLES-2], label="Default", colors='r')

# Setup axis
plt.xlim([x_time[0], x_time[N_SAMPLES-2]])

########################################################################################################################
plt.title("Best permutation discovered over time")
plt.ylabel("Throughput")
plt.xlabel("Seconds")
plt.legend()
plt.grid()

plt.show()
# plt.savefig(DATA_OUTPUT + 'linux-nginx_discovery_overtime_no-tf.pdf')
