#!/bin/sh

if [ $# -ne 1 ]; then
	echo "Usage: $0 <day number>"
	exit 1
fi

DAYNUM=$1
NEWDAY="Day$DAYNUM"
INFILE="$NEWDAY"
INFILE+="In.txt"
PYFILE="$NEWDAY"
PYFILE+=".py"
mkdir $NEWDAY
touch "$NEWDAY/$INFILE"
echo "#!/usr/bin/python" > "$NEWDAY/$PYFILE"
chmod +x $NEWDAY/$PYFILE
echo "Day $DAYNUM added"
