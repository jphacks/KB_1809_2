#!/usr/bin/env bash

ENV_DIR=env_files

function backUpEnv {
    ENV_FILE=${ENV_DIR}/$1
    if [ -f ${ENV_FILE} ]; then
        echo "Backup ${ENV_FILE}"
        mv -f ${ENV_FILE} ${ENV_FILE}.bk
    fi
}

function restoreEnv {
    ENV_FILE=${ENV_DIR}/$1
    if [ -f ${ENV_FILE}.bk ]; then
        echo "Restore ${ENV_FILE}"
        mv -f ${ENV_FILE}.bk ${ENV_FILE}
    fi
}

if [ -d ${ENV_DIR}/data ]; then
    echo "Backup ${ENV_DIR}/data"
    mv ${ENV_DIR}/data ${ENV_DIR}/data_bk
    mkdir ${ENV_DIR}/data
fi

backUpEnv api.env
backUpEnv db.env
backUpEnv static.env

cat << EOS > ${ENV_DIR}/api.env
SECRET_KEY=djangotestsecretkey
DEBUG=True
DB_HOST=plannap-db
DB_USER=root
DB_PASSWORD=root
DB_NAME=dev_db
EOS

cat << EOS > ${ENV_DIR}/db.env
MYSQL_ROOT_PASSWORD=root
MYSQL_USER=develop
MYSQL_PASSWORD=password
MYSQL_DATABASE=dev_db
EOS

touch ${ENV_DIR}/static.env

make qa-start

echo "Wait for launch..."
sleep 20

make qa-manage ARGS=migrate
make qa-manage ARGS=test

rm -rf ${ENV_DIR}/data
if [ -d ${ENV_DIR}/data_bk ]; then
    echo "Backup ${ENV_DIR}/data"
    mv ${ENV_DIR}/data_bk ${ENV_DIR}/data
fi

restoreEnv api.env
restoreEnv db.env
restoreEnv static.env

make qa-clean