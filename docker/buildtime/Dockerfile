FROM python:2.7-slim

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG COMPONENT
ARG SHARED_VOLUME

ARG BUILD_DIRECTORY="/tmp/.build"
ARG BUILD_EXECUTABLE="build.sh"

# build-essential is needed to compile C source code.
# zip is needed to archive the package.
RUN DEPENDENCIES="build-essential zip" && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends ${DEPENDENCIES}

RUN mkdir --parents ${SHARED_VOLUME} && \
    mkdir --parents ${BUILD_DIRECTORY}

WORKDIR ${BUILD_DIRECTORY}

COPY docker/buildtime/${BUILD_EXECUTABLE} .
COPY ${COMPONENT} ./${COMPONENT}
COPY requirements.txt .
COPY main.py .

RUN rm -fr /var/lib/apt/lists/*

VOLUME ${SHARED_VOLUME}

ENTRYPOINT ["./build.sh"]
