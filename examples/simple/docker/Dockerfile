# for base
FROM python:3.8-bullseye

ENV LANG C.UTF-8

WORKDIR /root/app

COPY ./docker/sources.list /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y \
    vim \
    iputils-ping \
    locales \
    logrotate \
    nginx \
    cron \
    && apt-get clean

COPY ./docker/.pip.conf /root/.pip/pip.conf

COPY ./docker/gunicorn /etc/logrotate.d/gunicorn

COPY ./docker/gunicorn.cron /etc/cron.d/gunicorn.cron
COPY ./docker/crond /etc/pam.d/crond

COPY ./docker/launch.sh /root/launch.sh

RUN chmod 0644 /etc/cron.d/gunicorn.cron
RUN chmod 777 /root/launch.sh
RUN touch /var/log/cron.log

COPY ./docker/nginx_default.conf /etc/nginx/sites-available/default
COPY ./docker/nginx.conf /etc/nginx/nginx.conf

# for project
WORKDIR /root/app

COPY ./requirements.txt ./requirements.txt
RUN pip3 install  --no-cache-dir -r ./requirements.txt

COPY ./ ./

RUN mkdir -p logs

ENTRYPOINT ["/root/launch.sh"]
CMD ["prod"]

