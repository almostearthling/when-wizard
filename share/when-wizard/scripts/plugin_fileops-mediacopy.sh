#!/bin/sh
# This script will copy all files from the media labeled as specified in first
# parameter to directory provided as the second parameter using rsync

SRC="$1"
DEST="$2"

if [ -d "$SRC" -a -d "$DEST" ]; then
    rsync -qrtv "$SRC/" "$DEST/"
fi