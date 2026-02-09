#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Daniel Oñoro Rubio
@organization: NEC Europe, Heidelberg, Germany.
@contact: daniel.onoro@neclab.eu
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Constants
DATA_FOLDER = "../data/"
OUTPUT_FOLDER = "../pdfs/"
FILES = [
    "hpc_feat_imp.csv",
    "redis_feat_imp.csv",
    "nginx_feat_imp.csv",
    "sqlite_feat_imp.csv"
]
CLASS_LABELS = ['NGINX', 'REDIS', 'SQLITE', 'HPC']
NUM_CLASSES = len(CLASS_LABELS)


def load_feature_data(files, data_folder):
    """Load feature importance data from CSV files.

    Args:
        files: List of CSV filenames to load
        data_folder: Directory containing the CSV files

    Returns:
        DataFrame with features as columns and applications as rows
    """
    data_dict = {}

    for filename in files:
        filepath = os.path.join(data_folder, filename)
        table = np.loadtxt(filepath, dtype='object', delimiter=',')

        for row_idx in range(table.shape[0]):
            feature_name = table[row_idx, 0]
            feature_value = float(table[row_idx, 1])

            if feature_name not in data_dict:
                data_dict[feature_name] = [feature_value]
            else:
                data_dict[feature_name].append(feature_value)

    # Filter to keep only features present in all files
    data_dict = {k: v for k, v in data_dict.items() if len(v) == NUM_CLASSES}

    return pd.DataFrame(data_dict)


def compute_similarity_matrix(data_df):
    """Compute pairwise similarity matrix using Euclidean distance.

    Args:
        data_df: DataFrame with applications as rows and features as columns

    Returns:
        Similarity matrix as numpy array
    """
    num_apps = len(data_df)
    similarity_matrix = np.zeros((num_apps, num_apps))

    for i in range(num_apps):
        for j in range(num_apps):
            diff = data_df.iloc[i] - data_df.iloc[j]
            distance = np.sqrt(np.sum(diff**2))
            similarity = 1.0 / (1.0 + distance)
            similarity_matrix[i, j] = similarity

    return similarity_matrix


def plot_similarity_heatmap(similarity_matrix, class_labels, output_path):
    """Create and save a heatmap visualization of the similarity matrix.

    Args:
        similarity_matrix: Square matrix of similarity values
        class_labels: Labels for each class
        output_path: Path where the plot should be saved
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create heatmap
    im = ax.imshow(similarity_matrix, cmap='coolwarm')

    # Configure axes
    ax.set_xticks(np.arange(len(class_labels)))
    ax.set_yticks(np.arange(len(class_labels)))
    ax.set_xticklabels(class_labels)
    ax.set_yticklabels(class_labels)

    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")

    # Add text annotations
    for i in range(len(class_labels)):
        for j in range(len(class_labels)):
            ax.text(j, i, f"{similarity_matrix[i, j]:.3f}",
                   ha="center", va="center", color="w")

    # Add title and colorbar
    ax.set_title("Application similarity matrix")
    plt.colorbar(im, ax=ax)

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    """Main execution function."""
    # Load data
    data_df = load_feature_data(FILES, DATA_FOLDER)

    # Compute similarity matrix
    similarity_matrix = compute_similarity_matrix(data_df)

    # Create output directory if needed
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Plot and save
    output_path = os.path.join(OUTPUT_FOLDER, "new_transfer_learning_mat.pdf")
    plot_similarity_heatmap(similarity_matrix, CLASS_LABELS, output_path)

    print(f"Similarity matrix plot saved to: {output_path}")


if __name__ == "__main__":
    main()