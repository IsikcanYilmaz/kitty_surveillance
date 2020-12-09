#!/bin/bash

# Short script to satisfy quick file transfers/synchronizations
# between main dev machine and raspberry pi

# This script will copy everything in $HOME/KODMOD/kitty_surveillance into
# the pi, to directory $HOME/kitty_surveillance

# USAGE:
# Have DST_ADDR set in your env variables to be the ip address of the pi
# Have DST_NAME set to be the hostname
# run by doing  $ ./sync.sh

# Have an environment variable to hold the pi's ip address
if [ -z "$DST_ADDR" ] || [ -z "$DST_NAME" ]; then
  echo "Set the env variable DST_ADDR to raspi's ip address."
  echo "Set the env variable DST_NAME to it's hostname"
  exit
else
  echo "SYNC $DST_NAME"@"$DST_ADDR"
fi

SRC="$HOME/kitty_surveillance_media" # Host
DST="/home/$DST_NAME/kitty_surveillance_media/*" # Pi

rsync -avz -e ssh $DST_NAME"@"$DST_ADDR:$DST $SRC # Pi to Host. Copy over contents of kitty_surveillance_media

SRC="$HOME/KODMOD/kitty_surveillance/*" # Host
DST="/home/$DST_NAME/kitty_surveillance/" # Pi

rsync -avz -e ssh $SRC $DST_NAME"@"$DST_ADDR:$DST # Host to Pi. Copy over code
