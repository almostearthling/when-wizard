#!/bin/sh
# send an e-mail message: the mailutils package *must* be installed and
# correctly configured (normally via "smarthost") during installation

TO="$1"
TITLE="$2"
MESSAGE="$3"

# do something with that stuff
echo -e "Subject: $TITLE\n\n$MESSAGE\n.\n" | mail $TO

# end.
