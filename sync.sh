#!/bin/bash

# Short script to satisfy quick file transfers/synchronizations
# between main dev machine and raspberry pi

# Have an environment variable to hold the pi's ip address
if [ -z "$DST_ADDR" ] || [ -z "$DST_NAME" ]; then
  echo "Set the env variable DST_ADDR to raspi's ip address."
  echo "Set the env variable DST_NAME to it's hostname"
  exit
fi

SRC="$HOME/kitty_surveillance_media"
DST="/home/$DST_NAME/kitty_surveillance_media/*"

rsync -avz -e ssh $DST_NAME"@"$DST_ADDR:$DST $SRC

SRC="$HOME/KOMOD/kitty_surveillance_media/*"
DST="/home/$DST_NAME/kitty_surveillance/"

rsync -avz -e ssh $DST_NAME"@"$DST_ADDR:$DST $SRC
