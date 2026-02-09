#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    @author: Daniel Oñoro Rubio
    @organization: NEC Europe
    @contact: daniel.onoro@neclab.eu
    @date: Created at 2023-05-04
"""

import os
import matplotlib.pyplot as plt
import pandas as pd


# Constants
OUTPUT_FOLDER = '../pdfs/'
DATA_FOLDER = '../data/'
DATA_FILE = os.path.join(DATA_FOLDER, 'unikraft-nginx_policy.csv')
N_SAMPLES = 500
DEFAULT_VALUE = 40720
X_LIMIT = 12000
Y_LIMIT = 55000
SHADE_ALPHA = 0.3


def plot_experiment_line(df, time_col, mean_col, std_col, label):
    """Plot a line with shaded standard deviation region."""
    plt.plot(df[time_col], df[mean_col], label=label)

    lower_bound = df[mean_col] - df[std_col]
    upper_bound = df[mean_col] + df[std_col]
    plt.fill_between(df[time_col], lower_bound, upper_bound, alpha=SHADE_ALPHA)

    return df[time_col]


def main():
    """Generate unikraft-nginx policy comparison plot."""
    # Read data
    plot_df = pd.read_csv(DATA_FILE)

    # Plot Random experiment
    plot_experiment_line(
        plot_df, 'test_tm', 'rng_tp_mean', 'rng_tp_std', 'Random'
    )

    # Plot Bayesian optimization
    plot_experiment_line(
        plot_df, 'bayes-opt_tm', 'bayes-opt_tp_mean', 'bayes-opt_tp_std', 'Bayesian-opt'
    )

    # Plot Wayfinder (deepTune)
    x_time = plot_experiment_line(
        plot_df, 'deeptune_tm', 'deeptune_tp_mean', 'deeptune_tp_std', 'Wayfinder'
    )

    # Plot default value baseline
    plt.hlines(
        DEFAULT_VALUE,
        xmin=0,
        xmax=x_time.iloc[N_SAMPLES - 2],
        label="Default",
        colors='r'
    )

    # Configure plot
    plt.xlim([0, X_LIMIT])
    plt.ylim(0, Y_LIMIT)
    plt.title('Average sampling policy learning')
    plt.ylabel('Throughput')
    plt.xlabel('Seconds')
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Save plot
    output_path = os.path.join(OUTPUT_FOLDER, 'new_unikraft-nginx-sampling_policy.pdf')
    plt.savefig(output_path)


if __name__ == '__main__':
    main()
