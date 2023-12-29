FROM python:3.11-alpine3.18 AS builder

MAINTAINER usharerose

# Setup basic Linux packages
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
    apk update && \
    apk add --no-cache tini tzdata build-base libffi-dev make && \
    apk upgrade && \
    rm -rf /var/cache/apk/*

# Setup base folder
RUN addgroup -S -g 1000 swish && \
    adduser -S -G swish -u 1000 swish && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    mkdir -p /home/swish/ && \
    mkdir -p /services/swish/

# Set workdir
WORKDIR /services/swish/swish-acquisition/

COPY . .

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # no virtual env need for container
    POETRY_VIRTUALENVS_CREATE=false

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# install dependencies
RUN python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip install --no-cache --upgrade pip && \
    python -m pip install --no-cache poetry==${POETRY_VERSION} && \
    poetry install --no-cache && \
    find /usr/local/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

# Add PYTHONPATH
ENV PYTHONPATH /services/swish/swish-acquisition/

FROM python:3.11-alpine3.18 AS prod

COPY --from=builder /etc/ /etc/
COPY --from=builder /usr/ /usr/
COPY --from=builder --chown=swish:swish --chmod=750 /home/swish/ /home/swish/
COPY --from=builder --chown=swish:swish --chmod=750 /services/swish/swish-acquisition/ /services/swish/swish-acquisition/
COPY --from=builder /sbin/ /sbin/

# Set workdir
WORKDIR /services/swish/swish-acquisition/

# User must be swish
USER swish

# Tini is now available at /sbin/tini
ENTRYPOINT ["/sbin/tini", "--"]

CMD ["sleep", "infinity"]
