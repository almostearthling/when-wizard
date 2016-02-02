#!/bin/sh
# This script will copy all files from the media labeled as specified in first
# parameter to directory provided as the second parameter using rsync

MEDIA="$1"
DEST="$2"

rsync -qrtv "/media/$MEDIA/" "$DEST/"
