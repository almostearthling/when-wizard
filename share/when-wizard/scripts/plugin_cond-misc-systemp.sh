#!/bin/sh
# calculate an average temperature based on sensor readings, and compare it
# to a specified Celsius temperature

TARGET="$1"

SENSOR_TEMPS=`sensors -u | fgrep _input | awk '{print $2}' | cut -d'.' -f1`
ITEMS=0
SUM=0
for x in $TEMPS ; do
    ITEMS=$(($ITEMS + 1))
    SUM=$(($SUM + $x))
done

# for now we just optimistically discard decimals
AVERAGE=`bc -l <<< "scale=3;$SUM/$ITEMS" | cut -d'.' -f1`

# only succeed if target temperature is reached
if [ "$AVERAGE" -lt "$TARGET" ]; then
    exit 1
fi

# end.
