FROM        python:3.8-slim as devstage

ENV         LANG C.UTF-8
ENV         USER app
ENV         PROJECTPATH=/home/app/messanger

RUN         set -x \
            && apt-get -qq update \
            && apt-get install -y --no-install-recommends \
               libpq-dev git gcc python3-dev \
            && apt-get purge -y --auto-remove \
            && rm -rf /var/lib/apt/lists/*

RUN         useradd -m -d /home/${USER} ${USER} \
            && mkdir -p /home/${USER}/logs/ \
            && chown -R ${USER} /home/${USER}

COPY        ./requirements.txt ${PROJECTPATH}/

RUN         pip install --upgrade pip \
            && pip install -U pytest celery \
            && pip install --no-cache-dir -r ${PROJECTPATH}/requirements.txt

ADD         https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait ${PROJECTPATH}/wait
RUN         chmod +x ${PROJECTPATH}/wait

COPY        . ${PROJECTPATH}

WORKDIR      ${PROJECTPATH}
USER         ${user}