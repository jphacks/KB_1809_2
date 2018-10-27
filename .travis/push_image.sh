#!/usr/bin/env bash

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    if [ "$TRAVIS_BRANCH" == "$DEPLOY_BRANCH" ]; then
        docker push studioaquatan/plannap-api:latest
    fi
fi