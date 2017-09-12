ARG VERSION
FROM dnguyen0304/roomlistwatcher-runtime:${VERSION}

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG NAMESPACE

ARG BUILDTIME_DEPENDENCIES="unzip"
ARG PACKAGE="${NAMESPACE}-latest.zip"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends ${BUILDTIME_DEPENDENCIES}

COPY ${PACKAGE} .

RUN unzip -q ${PACKAGE} && \
    chown --recursive ${NAMESPACE}:${NAMESPACE} . && \
    rm ${PACKAGE}

RUN rm -fr /var/lib/apt/lists/* && \
    apt-get purge -y --auto-remove ${BUILDTIME_DEPENDENCIES}

ENTRYPOINT ["python", "./main.py"]
