#!/bin/sh
# determine system load and compare it to a given percentage

TARGET=$1

# find load average in the last minute as an integer
LOAD_LAST=`cut -d' ' -f1 /proc/loadavg`
LOAD_AVG=`bc -l <<< "100 * $LOAD_LAST" | cut -d'.' -f1`

# condition is verified (script is successful) only if target usage is reached
if [ "$LOAD_AVG" -lt "$TARGET" ]; then
    exit 1
fi

# end.
