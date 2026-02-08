# Experiment for Figure 1

This script allows to regenerate Figure 1, showing the evolution of the number of compile-time (Kconfig) options of Linux throughout time.

## Prerequisites

You need the `matplotlib` Python library installed to run the script.
To install it, you can use pip:

```bash
pip install -r requirements.txt
```

## Running the Experiment

For that use the following script:

```bash
./regenerate-fig1.sh
```

The script will clone the entire Linux git repository and count, for each tag, the number of Kconfig options.
This can take a few minutes.
These results will go into a file named `results.csv`, showing for each tag its date, tag name, and number of Kconfig options.

```ascii
2026/02/01_22:01:13 v6.19-rc8 21500
2026/01/25_22:11:24 v6.19-rc7 21501
2026/01/18_23:42:45 v6.19-rc6 21501
2026/01/12_03:03:14 v6.19-rc5 21501
2026/01/04_22:41:55 v6.19-rc4 21501
2025/12/28_21:24:26 v6.19-rc3 21501
2025/12/21_23:52:04 v6.19-rc2 21501
2025/12/14_04:05:07 v6.19-rc1 21501
2025/11/30_22:42:10 v6.18 21334
2025/11/23_22:53:16 v6.18-rc7 21334
2025/11/16_22:25:38 v6.18-rc6 21334
2025/11/09_23:10:19 v6.18-rc5 21332
2025/11/02_19:28:02 v6.18-rc4 21331
```

Populating `results.csv` also takes a few minutes, you can monitor the progress by looking at the file.
The script will work its way back in time from the most recent tag up to the oldest one.

The script will then invoke `plot_results.py` which transforms this data into a graph, `linux-options.pdf`.

> [!IMPORTANT]
> The graph will differ slightly from what is in the paper as when we originally generated it (2023) the latest version of Linux was `v6.4-rc7`.
