#!/bin/bash
cd "$(dirname "$0")"
docker build -t tapiocafox/us:latest .
docker run --network dns_network --name us -p 8080:8080 -it tapiocafox/us
docker stop us
docker rm us