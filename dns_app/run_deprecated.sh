#!/bin/bash
./AS/run.sh &
as_pid=$!

./FS/run.sh &
fs_pid=$!

./US/run.sh &
us_pid=$!

wait $as_pid
wait $fs_pid
wait $us_pid

echo "All services have stopped."