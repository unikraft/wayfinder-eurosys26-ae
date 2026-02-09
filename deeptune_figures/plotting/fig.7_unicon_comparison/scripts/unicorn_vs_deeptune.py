#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compare Unicorn vs DeepTune scalability metrics.

@author: Daniel Oñoro Rubio
@organization: NEC Europe, Heidelberg, Germany.
@contact: daniel.onoro@neclab.eu
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Constants
DATA_FOLDER = Path(__file__).parent.parent / "data"
OUTPUT_FOLDER = Path(__file__).parent.parent / "pdfs"
UNICORN_FILE = DATA_FOLDER / "unikorn_mem-time_vs_it.csv"
DEEPTUNE_FILE = DATA_FOLDER / "deeptune_samples-mem-time.csv"


def load_data():
    """Load Unicorn and DeepTune data from CSV files."""
    unicorn_df = pd.read_csv(UNICORN_FILE)
    deeptune_df = pd.read_csv(DEEPTUNE_FILE)
    return unicorn_df, deeptune_df


def align_data(unicorn_df, deeptune_df):
    """Align both datasets by number of samples."""
    n_samples_idx = unicorn_df['n_samples'].astype('int')

    data = {
        'n_samples': n_samples_idx,
        'mem_unicorn': unicorn_df['mem'],
        'mem_deeptune': deeptune_df['memory'].iloc[n_samples_idx].values,
        'time_unicorn': unicorn_df['time'],
        'time_deeptune': deeptune_df['time'].iloc[n_samples_idx].values
    }
    return data


def plot_comparison(data, metric, ylabel, ax):
    """Plot comparison for a single metric."""
    ax.plot(data['n_samples'], data[f'{metric}_unicorn'], label="Unicorn")
    ax.plot(data['n_samples'], data[f'{metric}_deeptune'], label="DeepTune")
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Number of samples')
    ax.grid()
    ax.legend()


def create_plots(data, output_path):
    """Create and save comparison plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    plot_comparison(data, 'mem', 'Measured memory (Bytes)', ax1)
    plot_comparison(data, 'time', 'Measured time (seconds)', ax2)

    fig.tight_layout(pad=1.0)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def main():
    """Main execution function."""
    unicorn_df, deeptune_df = load_data()
    data = align_data(unicorn_df, deeptune_df)
    output_path = OUTPUT_FOLDER / "new_scalability.pdf"
    create_plots(data, output_path)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    main()

