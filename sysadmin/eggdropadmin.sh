#!/bin/sh

# Administer an Eggdrop bot

NAME="Eggdrop [dr-robotnik]"
DIR="/home/user/bots/dr-robotnik/"
CONFIG="dr-robotnik.conf"
PORT=12345
PIDFILE="pid.dr-robotnik"
EDITOR="joe"
LOGFILE="logs/dr-robotnik.log"

case "$1" in
    start)
        echo "Starting $NAME..."
        cd $DIR
        ./$CONFIG
        cd ~/
        echo "Done."
        ;;
    stop)
        echo "Searching pid..."
        cd $DIR
        if [ -f $PIDFILE ]; then
            PID=$(cat $PIDFILE)
            echo "Found pid $PID"
            echo "Stopping $NAME..."
            kill -9 $PID
            echo "Done."
        else
            echo "Could not get pid."
        fi
        cd ~/
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    admin)
        echo "Connecting to $NAME on port $PORT..."
        telnet localhost $PORT
        ;;
    conf)
        echo "Editing config file..."
        $EDITOR $DIR$CONFIG
        ;;
    log)
        echo "Showing log..."
        less $DIR$LOGFILE
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|admin|conf|log}" >&2
        exit 2
        ;;
esac
exit 0
