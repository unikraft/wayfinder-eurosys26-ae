# Wayfinder Eurosys26 Artifact Evaluation


## Overview

This repository contains directories for the figures in the "Wayfinder: Automated Operating System Specialization"  paper.
Each directory contains a `README.md` file detailing how to run the experiment and fetch the data, or how to use the data to generate the figures in the paper.
This repository assumes that the `wfctl` tool exists and `wayfinder` is installed on the system.


## Wayfinder Setup

Setting up Wayfinder means compiling it and setting up all dependencies and configuration files properly to be able to run it.

This is already done and running on the evaluation server so this can be skipped.


### 1. Installation

To install Wayfinder, navigate to its [repository](https://github.com/unikraft/wayfinder) and clone it.
Use `go` in the wayfinder build container to generate the executable:

```bash
# Create the container environment for the builds
sudo make container

# Start the developer environment
sudo make devenv

# Build wayfinder
make
```


### 2. Tool Dependency Installation

In order for Wayfinder to function as presented in the paper you will need the following installed tools of older versions:

- Qemu 5.2.0
- Libvirt 7.4.0
- Docker


### 3. Wayfinder Configuration

At a minimum you will have to configure the following in the `config/wayfinderd.yaml` file:

- Free ports for every service
- `host_iface` to match the interface of the server
- `cpu_sets` to be used for running/building experiments. We usually leave the first one for the helper containers.
- `influx_token` for saving extra VM metrics from libvirt (optional, but stops spamming)

You can also configure the helper containers in the `docker-compose.yaml` file.
If you have cpu0 free from the Wayfinder set, you can set it here for reducing experiment noise.


## Wayfinder Running

To run Wayfinder, you need to first start the helper containers.
To do this you can use the `docker-compose` command below:

```bash
docker-compose up registry influxdb postgres redis
```

After everything is running, you can also start the Wayfinder daemon:

```bash
sudo ./scripts/wayfinder.sh
```


## Experiment Setup

Most experiments have separate images meaning that for each separate experiment images need to be built and pushed to the registry started above.
In order to build an image, we use the usual `docker` commands.

For example, if we want to build the `linux-nginx` example and make it usable we would need to do the following:

```bash
# Navigate to the example
cd ~/wayfinder/examples/linux-nginx

# Build the builder image
docker build -t localhost:5000/linux-nginx:latest --progress=plain -f Dockerfile.jessie .

# Push the image to the local registry
docker push localhost:5000/linux-nginx:latest

# Navigate to the support test container
cd ~/wayfinder/support/wrk

# Build the helper `wrk` container
docker build -t localhost:5000/wrk:latest --progress=plain -f Dockerfile .

# Push the image to the local registry
docker push localhost:5000/wrk:latest
```


## Wayfinder Usage

Experiments have scripts attached to them that wrap over the `wfctl` commands, but that can be also used directly.

To create a job out of job yaml file we would do:
```
~/wayfinder/dist/wfctl --server localhost:6000 create ~/wayfinder/examples/linux-cozart-nginx/job_only_runtime.yaml
```

To run the first permutation, on individual cores, for job 34, we would do:

```
~/wayfinder/dist/wfctl --server localhost:6000 start --isol-level full --isol-split both -l 1 -s grid 34
```

To run 10 random permutations for job 34 we would do:
```
~/wayfinder/dist/wfctl --server localhost:6000 start --isol-level full --isol-split both -l 10 -s random 34
```

We can use `rainfrog` or `psql` to inspect data live as it gets populated in the database.
We use cpu core isolation to make sure we bring result noise to a minimum.
If we want to use an external model to suggest permutations we can use the python sdk for this which is generated from the proto specifications.


## Conclusion

The paragraphs above detail how to build and use the Wayfinder Framework to execute jobs on a server.
Each figure experiment is described in their directory and can be run irrespective of these instructions as Wayfinder is already running on the system.
The previous steps are good for setting up Wayfinder on a new system.
