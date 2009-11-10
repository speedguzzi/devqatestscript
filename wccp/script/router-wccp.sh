#!/bin/sh

I=/usr/local/ios/72-spk9-124
D=/usr/bin/dynamips
$D $I -i 1 -r 128 -X -T 2001 -p 1:PA-4E \
# -C cfg.txt \
-s 1:0:linux_eth:t0 \
-s 1:1:linux_eth:t1 \
-s 1:2:linux_eth:eth2.100  
