#!/usr/bin/env bash

# normal deploy
COMMAND="cd /opt/KB_1809_2 && sudo git pull && make pull && docker-compose -f docker-compose.prod.yml up -d --build && make qa-manage ARGS=migrate"

# exec
ssh -o StrictHostKeyChecking=no -i /tmp/aquatan_studio deploy@aqua.aquatan.studio ${COMMAND}