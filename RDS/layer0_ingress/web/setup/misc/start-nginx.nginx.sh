#!/usr/bin/env bash
export EXISTING_VARS=$(printenv | awk -F= '{print $1}' | sed 's/^/\$/g' | paste -sd,);
for file in $JSFOLDER;
do
  mv $file $file.bak
  cat $file.bak | envsubst $EXISTING_VARS > $file
  rm $file.bak
done
nginx -g 'daemon off;'