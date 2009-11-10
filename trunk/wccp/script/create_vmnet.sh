#!/bin/sh

## $1 : vmnet id  ; 9 < id < 99
## $2 : interface name 

# remove vmnet 
rm -rf /dev/vmnet$1

# create vmnet
mknod -m 600 /dev/vmnet$1 c 119 $1

/usr/bin/vmnet-bridge -d /var/runvmnet-bridge-${1}.pid /dev/vmnet${1} $2

