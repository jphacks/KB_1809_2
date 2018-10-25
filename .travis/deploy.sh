#!/usr/bin/env bash

# normal deploy
START_SERVER="make prod-start"
MIGRATE="make prod-manage ARGS=migrate"
COMMAND="cd /opt/KB_1809_2 && sudo git pull && make pull && $START_SERVER && $MIGRATE"

# exec
ssh -o StrictHostKeyChecking=no -i /tmp/aquatan_studio deploy@aqua.aquatan.studio ${COMMAND}