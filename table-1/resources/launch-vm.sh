#!/bin/bash

qemu-system-x86_64 \
    -m 1G \
    -nographic \
    -nic user \
    -hda debian.qcow2 \
    -kernel linux/arch/x86_64/boot/bzImage \
    -append "console=ttyS0 root=/dev/sda1"
