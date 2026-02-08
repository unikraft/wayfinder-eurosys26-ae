# Experiment for Table 1

These scripts allow to reproduce Table 1 (Linux v6.0 configuration space).
The configuration space of Linux can be divided into compile-time options (Kconfig), boot time options (kernel command line parameters), and runtime options (`/proc/sys`, etc.).

## Prerequisites

You need docker installed in the command line.
To setup and start the container launch the following script:

```bash
./launch-container.sh
```

The rest of the commands in this guide must be run within the container.

## Counting Command Line Options

```bash
cd linux && bash ../count-option-types.sh && cd -
```

## Running the Experiment

### Counting Boot Time Options

These options are listed for [Linux v6.0](https://www.kernel.org/doc/html/v6.0/admin-guide/kernel-parameters.html).
So we can parse this page as follows:

```bash
wget -O - https://www.kernel.org/doc/html/v6.0/admin-guide/kernel-parameters.html | grep -P "^\s+[a-z]+=" | wc -l
```

### Counting Runtime Options

For that we need to boot a Linux 6.0 kernel.
Still inside the container, launch a Qemu VM:

```bash
./launch-vm.sh
```

Login as `root`, password `a`, then count the number of runtime options, i.e. the number of writable files in `/proc/sys` and `/sys`:

```bash
find /proc/sys /sys -type f -perm /222 2>/dev/null | wc -l
```

This number is not entirely deterministic and you may see slight variations with what is in the paper.

:::tip
The VM can be halted with the `halt` command, and Qemu exited with `ctrl+a` followed by `x`.
:::
