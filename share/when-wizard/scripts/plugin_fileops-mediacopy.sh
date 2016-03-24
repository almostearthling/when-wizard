#!/bin/sh
# This script will copy all files from the media labeled as specified in first
# parameter to directory provided as the second parameter using rsync

MEDIA="$1"
DEST="$2"
SRC="/media/$USER/$MEDIA"

notify-send -i drive-removable-media "Media Copy" "Synchronizing $SRC to $DEST"

if [ ! -d "$DEST" ] ; then
    mkdir -p "$DEST" || exit 2
fi

OUTCOME="failed"
sleep 3
if [ -d "$SRC" -a -d "$DEST" ] ; then
    OUTCOME="succeeded"
    rsync -qrtv "$SRC/" "$DEST/" || OUTCOME="failed"
fi

notify-send -i drive-removable-media "Media Copy" "Synchronization complete (operation $OUTCOME)."

if [ "$OUTCOME" = "failed" ] ; then
    exit 2
fi

# end.
