#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1

echo "------------------------------------"
echo "    install dtb_finder dependencies    "
echo "------------------------------------"

if [ "$1" = "fedora" ]
then 
	sudo -EH dnf install -y dtc || exit 1
else
	sudo -EH apt-get install -y device-tree-compiler || exit 1
fi


exit 0
