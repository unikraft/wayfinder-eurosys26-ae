#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    @author: Daniel Oñoro Rubio
    @organization: NEC Europe
    @contact: daniel.onoro@neclab.eu
    @date: Created at 2022-08-16
"""

import glob
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import generic_filter


# Constants
WAYFINDER_DATA_FOLDER = '../data/*.xlsx'
DATA_OUTPUT = '../pdfs/'
RANDOM_DATA_PATH = '../../../measurements/linux-riscv.xlsx'
MEM_TIME_DATA_PATH = '../data/n_samples-mem-time.csv'

N_SAMPLES = 128
WINDOW_SIZE = 100
TO_MB = 1 / 1000000
MAX_MEM = 214761472.0 * TO_MB
DEFAULT_MEM = 210000000 * TO_MB

# Redis timing data
REDIS_TIMES = [99.76, 87.04, 76.06, 70.30, 85.74, 87.43, 99.72, 117.24, 112.66, 71.66]


def load_and_process_random_data(filepath, n_samples):
    """Load random baseline data and process throughput values."""
    df = pd.read_excel(filepath)
    arg_idx = np.argsort(df['perm_id'])
    y = np.array(df['throughput'])[arg_idx][:n_samples]

    crash_idx = np.where(y == 1)[0]
    y = -y * TO_MB
    y[crash_idx] = MAX_MEM

    return y, crash_idx


def load_and_process_wayfinder_data(filepath, n_samples):
    """Load Wayfinder data and process throughput values."""
    df = pd.read_excel(filepath)
    arg_idx = np.argsort(df['perm_id'])
    y = np.array(df['throughput'])[arg_idx][:n_samples] * TO_MB

    crash_idx = np.where(y <= 0)[0]
    y = MAX_MEM - y
    y[crash_idx] = MAX_MEM

    return y, crash_idx


def apply_smoothing(y, window_size):
    """Apply moving average smoothing and calculate standard deviation."""
    y_smoothed = generic_filter(y, np.mean, size=window_size, mode='reflect')
    y_std = generic_filter(y, np.std, size=window_size, mode='reflect')
    return y_smoothed, y_std


def generate_random_times(redis_times, n_points):
    """Generate cumulative random times based on Redis timing statistics."""
    mean_time = np.mean(redis_times)
    std_time = np.std(redis_times)
    return np.cumsum(np.random.normal(mean_time, std_time, size=n_points))


def plot_data_with_uncertainty(x, y, y_std, crash_idx, label, marker='*'):
    """Plot data with uncertainty bands and crash markers."""
    plt.plot(x, y, label=label)

    lower_bound = y - y_std
    upper_bound = y + y_std
    plt.fill_between(x, lower_bound, upper_bound, alpha=0.3)

    if len(crash_idx) > 0:
        plt.plot(x[crash_idx], y[crash_idx], marker)


def main():
    """Main plotting function."""
    # Load and process random baseline data
    y_random, crash_idx_random = load_and_process_random_data(RANDOM_DATA_PATH, N_SAMPLES)
    y_random_smoothed, y_random_std = apply_smoothing(y_random, WINDOW_SIZE)

    # Generate random timing data
    x_time_random = generate_random_times(REDIS_TIMES, y_random_smoothed.shape[0])

    # Plot random baseline
    plot_data_with_uncertainty(
        x_time_random, y_random_smoothed, y_random_std,
        crash_idx_random, 'Random'
    )

    # Load and plot Wayfinder data
    results_file_list = glob.glob(WAYFINDER_DATA_FOLDER)

    for results_file in results_file_list:
        y_wayfinder, crash_idx_wayfinder = load_and_process_wayfinder_data(
            results_file, N_SAMPLES
        )
        y_wayfinder_smoothed, y_wayfinder_std = apply_smoothing(y_wayfinder, WINDOW_SIZE)

        # Load timing data and add to random baseline
        mem_time_df = pd.read_csv(MEM_TIME_DATA_PATH)
        x_time = x_time_random + mem_time_df['time'][:N_SAMPLES]

        # Plot Wayfinder results
        plot_data_with_uncertainty(
            x_time, y_wayfinder_smoothed, y_wayfinder_std,
            crash_idx_wayfinder, 'DeepTune'
        )

    # Add default line
    plt.hlines(DEFAULT_MEM, xmin=x_time[0], xmax=x_time[N_SAMPLES - 2],
               label="Default", colors='r')

    # Configure plot
    plt.xlim([x_time[0], x_time[N_SAMPLES - 2]])
    plt.title('Wayfinder sample policy average performance')
    plt.ylabel('MB consumption')
    plt.xlabel('Seconds')
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Save figure
    Path(DATA_OUTPUT).mkdir(parents=True, exist_ok=True)
    plt.savefig(DATA_OUTPUT + 'new_linux-riscv_sampling_policy.pdf')


if __name__ == '__main__':
    main()
