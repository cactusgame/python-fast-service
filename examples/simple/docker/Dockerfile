# for base
FROM python:3.8-bullseye

ENV LANG C.UTF-8

WORKDIR /root/app

COPY ./docker/sources.list /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -v -y \
    curl \
    vim \
    iputils-ping \
    locales \
    logrotate \
    nginx \
    cron \
    && apt-get clean

# 设置pip使用阿里云镜像
COPY ./docker/.pip.conf /root/.pip/pip.conf

# 设置lograte的配置
COPY ./docker/gunicorn /etc/logrotate.d/gunicorn

# 启用lograte的定时任务
COPY ./docker/gunicorn.cron /etc/cron.d/gunicorn.cron
COPY ./docker/crond /etc/pam.d/crond

# 启动命令
COPY ./docker/launch.sh /root/launch.sh

RUN chmod 0644 /etc/cron.d/gunicorn.cron
RUN chmod 777 /root/launch.sh
RUN touch /var/log/cron.log

# 拷贝nginx配置
COPY ./docker/nginx_default.conf /etc/nginx/sites-available/default
COPY ./docker/nginx.conf /etc/nginx/nginx.conf

# for project
WORKDIR /root/app

# 安装算法依赖包
COPY ./setup/requirements.txt setup/requirements.txt
RUN pip3 install  --no-cache-dir -r setup/requirements.txt

# 源代码等
COPY ./ ./

# 必须创建日志目录
RUN mkdir -p logs

# 启动服务。本地调试时，可以覆盖启动命令
ENTRYPOINT ["/root/launch.sh"]
CMD ["prod"]

