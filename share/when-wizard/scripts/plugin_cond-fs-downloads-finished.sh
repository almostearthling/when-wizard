#!/bin/sh
# Check that there are no more downloads pending from the major browsers
# monitoring the known partial download file specifications in the provided
# download directory. It returns 0 if downloads *finished* (that is, there
# *were* active downloads and there are no more), and 1 otherwise; it expects
# to have one parameter pointing to the directory to be monitored.

DOWNLOADS="$1"
EXTENSIONS="crdownload part"
DONTCHECK="$DOWNLOADS/.cond-downloads-finished_skip-check.tmp"

discard_out () {
  $@ > /dev/null 2>&1
}

# the first time this is run it has to create a control file
if [ ! -f $DONTCHECK ] ; then
    echo "true" > $DONTCHECK
fi

# verify whether or not there are partials and if checks have to be skipped
skip=`cat $DONTCHECK`
partials="false"
for ext in $EXTENSIONS ; do
    if discard_out ls "$DOWNLOADS/*.$x" ; then
        partials="true"
    fi
done

# if there are any partials the checks must be enabled, so that when no
# more partials are present a success code can be returned
if [ "$partials" = "true" ] ; then
    echo "false" > $DONTCHECK
else
    echo "true" > $DONTCHECK
    if [ "$skip" = "false" ]; then
        exit 0
    fi
fi

# finally return a 1 error code
exit 1

# end.
