#!/bin/sh

# Manage (i.e. start/stop/restart) a daemon process.
#
# The process is first notified to shut down by a SIGTERM.
# If it is still alive after a 3 seconds, a SIGKILL is sent.

PIDFILE="daemon.pid"

case "$1" in
    start)
        echo "Starting daemon..."
        # Example call. Replace with your application.
        example_program --daemon --pid-file=$PIDFILE
        ;;
    stop)
        if [ ! -f $PIDFILE ]; then
            echo "Could not get pid, $PIDFILE not found."
        else
            PID=`cat $PIDFILE`
            kill -0 $PID 2> /dev/null
            if [ $? -ne 0 ]; then
                echo "Daemon not running."
            else
                echo "Found pid $PID, stopping daemon..."
                kill $PID
                for i in {0..3}; do
                    kill -0 $PID 2> /dev/null
                    if [ $? -eq 0 ]; then
                        break
                    fi
                    sleep 1
                done
                kill -kill $PID 2> /dev/null
                echo "Done."
            fi
        fi
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}" >&2
        exit 2
        ;;
esac
