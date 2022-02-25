#!/bin/bash
#
# A bash script to install requirement python3 libraries to fedora linux
echo "opencv, numpy and scipy are installing..."
sleep 1
sudo dnf install python3-opencv python3-numpy python3-scipy
echo "done!"
exit
