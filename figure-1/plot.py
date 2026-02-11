#!/usr/bin/python3

import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

INPUT="results.csv"
OUTPUT="linux-options.pdf"

font = {'size'   : 12}

matplotlib.rc('font', **font)

if __name__ == "__main__":
    options = []
    versions = []

    with open(INPUT) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=" ")

        counter = 0
        for row in csvreader:
            # Don't consider release candidates
            if "rc" in row[1]:
                continue

            options.append(int(row[2]))
            versions.append(row[1])

    # Result file is ordered in time
    options.reverse()
    versions.reverse()

    fig, ax = plt.subplots(1,1)
    ax.xaxis.set_major_locator(ticker.LinearLocator(numticks=15))
    plt.xticks(rotation = 30)

    plt.ylim(bottom=0, top=25000)
    plt.ylabel("Number of Linux\nKconfig compile-time\noptions")
    plt.xlabel("Linux version")

    fig.set_size_inches(6, 2.5)
    plt.plot(versions, options)
    plt.tight_layout()
    plt.grid()

    plt.savefig(OUTPUT)
    os.system("pdfcrop " + OUTPUT + " " + OUTPUT)
