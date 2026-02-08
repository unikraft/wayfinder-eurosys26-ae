#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python plot_results.py <baseline_file.csv> <random_file.csv>")
        sys.exit(1)

    # Read CSV files from command line arguments
    baseline_file = sys.argv[1]
    random_file = sys.argv[2]

    # Read baseline data and calculate average
    df_baseline = pd.read_csv(baseline_file)
    baseline_avg = df_baseline['value_float'].mean()

    # Read random data
    df_random = pd.read_csv(random_file)

    # Remove 0 values from random data
    df_random = df_random[df_random['value_float'] != 0]

    # Calculate average per permutation_id
    random_avgs = df_random.groupby('permutation_id')['value_float'].mean()

    # Sort the averages
    random_avgs_sorted = random_avgs.sort_values()

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the sorted random averages as a blue line
    plt.plot(range(len(random_avgs_sorted)), random_avgs_sorted.values,
             'b-', label='Nginx throughput (req/s)')

    # Plot the baseline average as a horizontal dotted line
    plt.axhline(y=baseline_avg, color='r', linestyle='--',
                label=f'Default configuration throughput')

    # Set labels and title
    plt.xlabel('Configuration #')
    plt.ylabel('Nginx throughput (req/s)')

    # Set Y axis to start at 0 with padding at the top
    max_value = max(random_avgs_sorted.max(), baseline_avg)
    plt.ylim(bottom=25000, top=max_value * 1.1)

    # Add legend in bottom right
    plt.legend(loc='lower right')

    # Add grid
    plt.grid(True, alpha=0.3)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('figure-2.png', dpi=300, bbox_inches='tight')
    print(f"Plot saved as figure-2.png")

if __name__ == '__main__':
    main()
