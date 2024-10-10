#!/bin/bash
cd "$(dirname "$0")"
docker build -t tapiocafox/fs:latest .
docker run --network dns_network --name fs -p 9090:9090 -it tapiocafox/fs
docker stop fs
docker rm fs