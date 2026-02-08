FROM debian:12

RUN apt update
RUN apt install -y git wget qemu-system-x86 build-essential flex libelf-dev bison bc libssl-dev libguestfs-tools

# Linux
RUN cd /root && git clone --depth=1 --branch=v6.0 https://github.com/torvalds/linux.git
RUN cd /root/linux && make x86_64_defconfig && make -j4

# Debian VM
COPY resources/extract-runtime-options.sh /root
RUN chmod +x /root/extract-runtime-options.sh

RUN cd /root && virt-builder debian-12 -o debian.qcow2 --format qcow2 --size 10G --hostname debian --root-password password:a --upload /root/extract-runtime-options.sh:/root/extract-runtime-options.sh

# Script to count the number of Kconfig options
COPY resources/count-option-types.sh /root
RUN chmod +x /root/count-option-types.sh

COPY resources/launch-vm.sh /root
RUN chmod +x /root/launch-vm.sh

WORKDIR /root
