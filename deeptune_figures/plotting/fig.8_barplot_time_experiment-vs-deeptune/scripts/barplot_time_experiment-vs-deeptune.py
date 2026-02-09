#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Barplot comparison of test times for different applications vs deepTune update time.

@author: Daniel Oñoro Rubio
@organization: NEC Europe
@contact: daniel.onoro@neclab.eu
@date: Created at 2023-05-12
"""
import os.path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

OUTPUT_FOLDER = '../pdfs'
OUTPUT_FILENAME = 'new_test_time-vs-deepTune_time.pdf'


def calculate_statistics(data: Dict[str, List[float]]) -> Tuple[List[str], List[float], List[float]]:
    """
    Calculate mean and standard deviation for each dataset.

    Args:
        data: Dictionary mapping application names to their timing measurements

    Returns:
        Tuple of (labels, means, stds)
    """
    labels = []
    means = []
    stds = []

    for label, values in data.items():
        labels.append(label)
        means.append(np.mean(values))
        stds.append(np.std(values))

    return labels, means, stds


def create_barplot(labels: List[str], means: List[float], stds: List[float],
                   output_path: str) -> None:
    """
    Create and save a barplot with error bars.

    Args:
        labels: Application names
        means: Mean values for each application
        stds: Standard deviations for each application
        output_path: Path to save the output PDF
    """
    x_pos = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.5,
           ecolor='black', capsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Time (s)')
    ax.set_title('Average test time of different applications vs deepTune update time')
    ax.grid(axis='y', alpha=0.3)

    # Annotate the last bar (deepTune)
    last_idx = len(means) - 1
    ax.text(last_idx, means[last_idx] + 1.5,
            f"{means[last_idx]:.2f}±{stds[last_idx]:.2f}",
            color='blue', fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    """Main execution function."""
    # Data measurements
    timing_data = {
        'nginx': [92.80, 92.80, 92.81, 92.72, 92.82, 92.76, 92.74,
                  42.69, 42.70, 42.71, 43.30],
        'redis': [150.49, 72.53, 72.56, 65.01, 67.57, 85.04, 72.60,
                  45.09, 45.03, 45.04, 45.02],
        'sqlite': [118.39, 45.49, 45.51, 45.52, 45.56, 78.10, 45.52,
                   44.21, 43.04, 42.98, 43.05, 43.07],
        'hpc': [72.44, 72.21, 74.82, 122.35, 122.31, 137.43, 132.34,
                122.30, 34.73, 34.66, 34.78, 34.76],
        'deepTune': [0.85]  # Single value with predefined std
    }

    # Calculate statistics
    labels, means, stds = calculate_statistics(timing_data)

    # Override deepTune std with predefined value
    stds[-1] = 0.1

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Generate and save plot
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    create_barplot(labels, means, stds, output_path)


if __name__ == '__main__':
    main()