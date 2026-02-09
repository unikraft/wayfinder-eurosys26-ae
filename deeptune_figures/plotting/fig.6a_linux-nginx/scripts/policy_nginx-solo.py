#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NGINX Sampling Policy Visualization

This script generates performance comparison plots for NGINX tuning strategies:
- Random sampling baseline
- DeepTune (no transfer learning)
- DeepTune with transfer learning (TL)

@author: Daniel Oñoro Rubio
@organization: NEC Europe
@contact: daniel.onoro@neclab.eu
@date: Created at 2022-08-16
"""

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import generic_filter

# Set random seed for reproducibility
np.random.seed(42)

# Configuration constants
WAYFINDER_DATA_FOLDER = '../data'
WAYFINDER_TL_DATA_FOLDER = 'linux-nginx_redis-tl'
DATA_OUTPUT = '../pdfs/'
RANDOM_DATA_FILE = '../../../measurements/linux-nginx_313_only_OS_single_core.xlsx'

N_SAMPLES = 250
N_TRIALS = 5
SMOOTHING_WINDOW = 100
DEFAULT_VALUE = 15731

# Plot styling
FIGSIZE = (6.4, 3.5)
Y1_LIMITS = (4000, 19000)
Y2_LIMITS = (0.02, 0.4)
ALPHA = 0.1


def smooth_signal(data, window_size):
    """Apply smoothing filter to data using moving average.
    
    Args:
        data: Input array to smooth
        window_size: Size of the smoothing window
        
    Returns:
        Smoothed data array
    """
    return generic_filter(data, np.mean, size=window_size, mode='reflect')


def simulate_random_baseline(data_file, n_samples, n_trials, time_samples):
    """Simulate random sampling baseline performance.
    
    Args:
        data_file: Path to baseline data Excel file
        n_samples: Number of samples to use
        n_trials: Number of trials to simulate
        time_samples: Time values for recorded runs
        
    Returns:
        Tuple of (time_data, experiment_data)
    """
    df = pd.read_excel(data_file)
    throughput = np.array(df['throughput'])
    
    # Generate time data from recorded runs
    mean_time = np.mean(time_samples)
    std_time = np.std(time_samples)
    time_random = np.cumsum(np.random.normal(mean_time, std_time, size=n_samples))
    
    # Simulate multiple trials with random shuffling
    experiment_data = []
    for _ in range(n_trials):
        experiment_data.append(throughput[:n_samples].copy())
        np.random.shuffle(throughput)
    
    return time_random, np.vstack(experiment_data)


def load_experiment_data(data_folder, subfolder=None, n_samples=N_SAMPLES):
    """Load experiment data from Excel files and corresponding time data.
    
    Args:
        data_folder: Base folder containing experiment data
        subfolder: Optional subfolder name
        n_samples: Number of samples to load
        
    Returns:
        Tuple of (experiment_data, time_data)
    """
    search_path = os.path.join(data_folder, subfolder, '*.xlsx') if subfolder else os.path.join(data_folder, '*.xlsx')
    results_files = glob.glob(search_path)
    
    experiment_data = []
    time_data = []
    
    for results_file in results_files:
        # Load throughput data
        df = pd.read_excel(results_file)
        sorted_idx = np.argsort(df['perm_id'])
        throughput = np.array(df['throughput'])[sorted_idx][:n_samples]
        experiment_data.append(throughput)
        
        # Load time data
        exp_id = os.path.basename(results_file)[-6]
        time_filename = f'n_samples-mem-time_{exp_id}.csv'
        time_path = os.path.join(data_folder, subfolder, time_filename) if subfolder else os.path.join(data_folder, time_filename)
        time_df = pd.read_csv(time_path)
        time_data.append(np.array(time_df['time'])[:n_samples])
    
    return np.vstack(experiment_data), np.vstack(time_data)


def compute_statistics(data):
    """Compute mean, std, and confidence bounds for experiment data.
    
    Args:
        data: 2D array of experiment data (trials x samples)
        
    Returns:
        Tuple of (mean, std, lower_bound, upper_bound)
    """
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    lower = mean - std
    upper = mean + std
    return mean, std, lower, upper


def plot_performance_with_crashes(ax1, ax2, time_data, performance_data, color, label, window_size):
    """Plot performance metrics and crash rates on dual axes.
    
    Args:
        ax1: Primary axis for throughput
        ax2: Secondary axis for crash rate
        time_data: Time values
        performance_data: Performance data array
        color: Plot color
        label: Plot label
        window_size: Smoothing window size
    """
    mean, std, lower, upper = compute_statistics(performance_data)
    
    # Smooth the signals
    mean_smooth = smooth_signal(mean, window_size)
    lower_smooth = smooth_signal(lower, window_size)
    upper_smooth = smooth_signal(upper, window_size)
    
    # Plot throughput
    ax1.plot(time_data, mean_smooth, color=color, label=label)
    ax1.fill_between(time_data, lower_smooth, upper_smooth, color=color, alpha=ALPHA)
    
    # Plot crash rate
    crash_vector = performance_data <= 0
    mean_crash = np.mean(crash_vector, axis=0)
    mean_crash_smooth = smooth_signal(mean_crash, window_size)
    ax2.plot(time_data, mean_crash_smooth, color=color, linestyle='dashed', label=f'{label} crash')


def setup_plot():
    """Create and configure the plot with dual y-axes.
    
    Returns:
        Tuple of (fig, ax1, ax2)
    """
    fig, ax1 = plt.subplots(figsize=FIGSIZE)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Throughput (req/s)')
    ax1.tick_params(axis='y')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Crash rate')
    ax2.tick_params(axis='y')
    
    fig.subplots_adjust(bottom=0.2)
    
    return fig, ax1, ax2


def main():
    """Main execution function."""
    # Setup plot
    fig, ax1, ax2 = setup_plot()
    
    # Recorded time samples from experiments
    time_samples = [92.80, 92.80, 92.81, 92.72, 92.82, 92.76, 92.74, 42.69, 42.70, 42.71, 43.30]
    
    # Generate random baseline
    time_random, random_data = simulate_random_baseline(RANDOM_DATA_FILE, N_SAMPLES, N_TRIALS, time_samples)
    plot_performance_with_crashes(ax1, ax2, time_random, random_data, 'r', 'Random', SMOOTHING_WINDOW)
    
    # Load and plot DeepTune (no TL)
    deeptune_data, deeptune_time = load_experiment_data(WAYFINDER_DATA_FOLDER)
    cumulative_time = np.cumsum(np.mean(deeptune_time, axis=0)) + time_random
    plot_performance_with_crashes(ax1, ax2, cumulative_time, deeptune_data, 'b', 'DeepTune', SMOOTHING_WINDOW)
    
    # Load and plot DeepTune with TL
    deeptune_tl_data, deeptune_tl_time = load_experiment_data(WAYFINDER_DATA_FOLDER, WAYFINDER_TL_DATA_FOLDER)
    cumulative_time_tl = np.cumsum(np.mean(deeptune_tl_time, axis=0)) + time_random
    plot_performance_with_crashes(ax1, ax2, cumulative_time_tl, deeptune_tl_data, 'g', 'DeepTune+TL', SMOOTHING_WINDOW)
    
    # Configure axis limits
    ax1.set_xlim([time_random[0], time_random[N_SAMPLES - 2]])
    ax2.set_xlim([time_random[0], time_random[N_SAMPLES - 2]])
    ax1.set_ylim(Y1_LIMITS)
    ax2.set_ylim(Y2_LIMITS)
    
    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, ncol=3)
    
    # Save figure
    os.makedirs(DATA_OUTPUT, exist_ok=True)
    output_path = os.path.join(DATA_OUTPUT, 'new_linux-nginx_sampling_policy_no-tf.pdf')
    plt.savefig(output_path)
    print(f"Plot saved to: {output_path}")


if __name__ == '__main__':
    main()



