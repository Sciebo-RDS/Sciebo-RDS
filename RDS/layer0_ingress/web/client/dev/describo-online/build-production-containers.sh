#!/usr/bin/env bash

if [ "$#" != 1 ] ; then
    echo "Please provide a version number for these containers: e.g. 0.1.0"
    exit -1
fi
VERSION="${1}"

read -p '>> Build the code? [y|N] ' resp
if [ "$resp" == "y" ] ; then
    echo '>> Building the API code'
    docker build --rm -t arkisto/describo-online-api:latest -f Dockerfile.api-build .
    echo

    echo '>> Building the UI code'
    cd ui
    # npm run build
    docker run -it --rm \
        -v $PWD:/srv/ui \
        -v $PWD/../../describo-ui-plugins:/srv/ui/src/plugins \
        -v ui_node_modules:/srv/ui/node_modules \
        -w /srv/ui node:14-buster bash -l -c "npm run build"
    cd -
    echo
fi

read -p '>> Build the containers? [y|N] ' resp
if [ "$resp" == "y" ] ; then
    echo "Building API container"
    docker tag arkisto/describo-online-api:latest arkisto/describo-online-api:${VERSION}
    # docker rmi $(docker images | grep none | awk '{print $3}')

    echo "Building UI container"
    docker build --rm -t arkisto/describo-online-ui:latest -f Dockerfile.ui-build .
    docker tag arkisto/describo-online-ui:latest arkisto/describo-online-ui:${VERSION}

    # docker rmi $(docker images | grep none | awk '{print $3}')
    echo
fi

read -p '>> Push the containers to docker hub? [y|N] ' resp
if [ "$resp" == "y" ] ; then
    echo "Pushing built containers to docker hub"
    docker login
    docker push arkisto/describo-online-api:latest
    docker push arkisto/describo-online-api:${VERSION}
    docker push arkistor/describo-online-ui:latest
    docker push arkisto/describo-online-ui:${VERSION}
fi