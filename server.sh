#!/bin/bash

LOGFILE="rclone_check.log"

# Run a test `rclone` command
if rclone lsd 3d_sync: > /dev/null 2>&1; then
    echo "$(date): Rclone is still connected." >> $LOGFILE
else
    echo "$(date): Rclone lost access! Attempting to reconnect..." >> $LOGFILE
    rclone config reconnect gdrive: >> $LOGFILE 2>&1
    drive_error.py
fi
