#!/bin/bash

PC2_IP=192.168.1.101

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${SCRIPT_DIR}/..

rsync -avzL \
    --exclude='venv' \
    --exclude='.*' \
    ../notebooklm2openai unitree@${PC2_IP}:~/