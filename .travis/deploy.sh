#!/usr/bin/env bash

# normal deploy
COMMAND="cd /opt/KB_1809_2 && make pull && make qa-manage ARGS=migrate && docker-compose up -d --build"

# exec
ssh -o StrictHostKeyChecking=no -i /tmp/aquatan_studio deploy@aqua.aquatan.studio ${COMMAND}