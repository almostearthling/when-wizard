#!/bin/sh
# This script will copy all files from the directory specified in first
# parameter to the directory provided as the second parameter using rsync

SRC="$1"
DEST="$2"

notify-send -i folder "Synchronization" "Synchronizing $SRC to $DEST"

if [ ! -d "$DEST" ] ; then
    mkdir -p "$DEST" || exit 2
fi

OUTCOME="failed"
sleep 3
if [ -d "$SRC" -a -d "$DEST" ] ; then
    rsync -qrtv "$SRC/" "$DEST/" || OUTCOME="failed"
fi

notify-send -i folder "Synchronization" "Synchronization complete (operation $OUTCOME)."

if [ "$OUTCOME" = "failed" ] ; then
    exit 2
fi

# end.
