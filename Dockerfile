FROM python:3.7.0-alpine3.8

ENV PROJECT_DIR /opt/plannap-api

COPY ./src ${PROJECT_DIR}
COPY Pipfile ${PROJECT_DIR}/Pipfile
COPY Pipfile.lock ${PROJECT_DIR}/Pipfile.lock

WORKDIR ${PROJECT_DIR}

RUN apk update && \
    apk add --no-cache \
        mariadb-dev \
        pcre-dev \
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev && \
        rm -rf /ver/cache/apk/*

RUN apk add --no-cache --virtual=build_dep \
        python3-dev \
        gcc \
        build-base \
        linux-headers \
        tzdata && \
    pip3 install pipenv && \
    pipenv install && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del --purge build_dep && \
    rm -rf /var/cache/apk/*

CMD ["pipenv", "run", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--proxy-protocol", "True", "plannap.wsgi"]