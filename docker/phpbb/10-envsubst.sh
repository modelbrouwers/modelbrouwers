#!/bin/sh

set -e

ME=$(basename $0)

template=/var/www/html/phpBB3/config.php.template
output_path=/var/www/html/phpBB3/config.php

defined_envs=$(printf '${%s} ' $(env | cut -d= -f1))
envsubst "$defined_envs" < "$template" > "$output_path"

exit 0
