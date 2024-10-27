#!/bin/bash
set -x

config_env=$1

if [ $config_env = "debug" ]; then
  # 1 month
  sleep 2592000
else
  cron
  nginx
  pfs $1
fi

