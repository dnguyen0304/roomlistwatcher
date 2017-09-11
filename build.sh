#!/usr/bin/env bash

set -eu

NAMESPACE="roomlistwatcher"
VERSION=$(grep -Po "version='\K\d\.\d\.\d" setup.py)
REMOTE_SHARED_VOLUME="/tmp/build"

rm --force ${NAMESPACE}*.zip

# Create the buildtime container.
docker build \
    --file docker/buildtime/Dockerfile \
    --tag ${NAMESPACE}-buildtime:${VERSION} \
    --build-arg COMPONENT=${NAMESPACE} \
    --build-arg SHARED_VOLUME=${REMOTE_SHARED_VOLUME} \
    .
# Create the package.
docker run \
    --volume $(pwd):${REMOTE_SHARED_VOLUME} \
    ${NAMESPACE}-buildtime:${VERSION} \
    ${NAMESPACE} ${REMOTE_SHARED_VOLUME} ${VERSION}

# Create the runtime container.
docker build \
    --file docker/runtime/Dockerfile \
    --tag dnguyen0304/${NAMESPACE}:${VERSION} \
    --build-arg NAMESPACE=${NAMESPACE} \
    --build-arg CONFIGURATION_FILE_NAME="application.config" \
    --build-arg AWS_CONFIGURATION_FILE_NAME="aws.config" \
    --build-arg AWS_CREDENTIALS_FILE_NAME="aws.credentials" \
    .
