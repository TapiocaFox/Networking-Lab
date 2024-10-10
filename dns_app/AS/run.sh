#!/bin/bash
cd "$(dirname "$0")"
docker build -t tapiocafox/as:latest .
docker run --network dns_network --name as -p 53553:53553 -it tapiocafox/as
docker stop as
docker rm as