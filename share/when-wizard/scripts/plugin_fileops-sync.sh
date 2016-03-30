#!/bin/sh
# This script will copy all files from the directory specified in first
# parameter to the directory provided as the second parameter using rsync

SRC="$1"
DEST="$2"


if [ ! -d "$DEST" ] ; then
    mkdir -p "$DEST" || exit 2
fi

OUTCOME="failed"
sleep 3
if [ -d "$SRC" -a -d "$DEST" ] ; then
    OUTCOME="succeeded"
    notify-send -i folder "Synchronization" "Synchronizing $SRC to $DEST"
    rsync -qrtv "$SRC/" "$DEST/" || OUTCOME="failed"
    notify-send -i folder "Synchronization" "Synchronization complete (operation $OUTCOME)."
fi


if [ "$OUTCOME" = "failed" ] ; then
    exit 2
fi

# end.
