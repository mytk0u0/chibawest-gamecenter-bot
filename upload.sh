#!/bin/bash

docker login
docker build -t mytk0u0/chibawest-gamecenter-bot .
docker push mytk0u0/chibawest-gamecenter-bot:latest