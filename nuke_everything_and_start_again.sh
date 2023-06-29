#!/usr/bin/env bash

datahub docker nuke
docker container prune
docker volume prune
docker system prune
datahub docker quickstart --version v0.10.4