# Experiment for Figure 2

Figure 2 of the paper shows the results of randomly searching for permutations of the linux kernel and benchmarking Nginx.
The experiment runs for 800 permutations with 3 repetitions each per permutation.
To calculate the baseline, 30 repetitions of the original configuration are run.

Estimated time to run the experiment: at least 30.375 hours.
To run the experiment faster, decrease the number of repetitions per permutation in the script, and/or decrease the number of permutations.

After obtaining the figure, you will notice numbers being much higher than the original experiment in the paper, as the server differs, but the relative difference between the baseline and the random search should be similar.
This results in a figure with a similar shape to the one in the paper, but with different absolute values.

## Building the environment

1. Create and push the builder image

```bash
# Navigate to the example
cd ~/wayfinder/examples/linux-nginx

# Build the builder image
docker build -t localhost:5000/linux-nginx:latest --progress=plain -f Dockerfile.jessie .

# Push the image to the local registry
docker push localhost:5000/linux-nginx:latest
```

2. Create and push the helper tool

```bash
# Navigate to the support test container
cd ~/wayfinder/support/wrk

# Build the helper `wrk` container
docker build -t localhost:5000/wrk:latest --progress=plain -f Dockerfile .

# Push the image to the local registry
docker push localhost:5000/wrk:latest
```

## Running the Experiment

1. Create the baseline experiment:

```bash
./create_experiment.sh
```

1. Start the baseline experiment:

```bash
./start_baseline.sh <experiment_id>
```

1. Create the random search experiment:

```bash
./create_experiment.sh
```

1. Start the random search experiment:

```bash
./start_random.sh <experiment_id>
```

1. Export the results:

```bash
./export_results.sh <experiment_id> results_random.csv
./export_results_baseline.sh <experiment_id> results_baseline.csv
```

1. Plot the results using the `plot_results.py` script:

```bash
python3 plot_results.py results_baseline.csv results_random.csv
```
