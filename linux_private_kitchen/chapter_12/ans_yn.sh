#!/bin/bash
# Program
#	This Program shows the user's choice.
# History
# 2019-07-16	FengHui		First Release

path=/bin:/sbin:/usr/bin:~/bin
export path

read -p "Please input (Y/N): " yn

[ "${yn}" == "Y" -o "${yn}" == "y" ] && echo "OK, continue" && exit 0
[ "${yn}" == "N" -o "${yn}" == "n" ] && echo "Oh, interrupt" && exit 0

echo "I dont't know what your choice is." && exit 0