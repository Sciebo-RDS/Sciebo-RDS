#!/bin/bash

cd ./charts/charts || exit
for d in */ ; do
    (
      echo "Going into dir: $d"
      cd "$d" || exit
      echo "Do helm build"
      helm dependency update
      helm dependency build
    )
done
echo "Done."
