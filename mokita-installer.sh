#!/bin/sh

# run get.osmosis.zone python script
curl -sL https:/github.com/gridiron-zone/merlin.git/install > i.py && python3 i.py

# after completion, source the profile
source ~/.profile
