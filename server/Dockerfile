# *** BEGIN common Dockerfile commands, to improve caching
# *** Please copy from Dockerfile.common
FROM python:3.7.9-buster

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y \
        libspatialindex-dev \
        postgresql-client \
        libopenblas-base \
        libomp-dev

# improve docker layer caching by installing requirements.txt early & separately
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install pip==21.1.1
RUN pip install -r requirements.txt

# *** BEGIN service-specific customizations
COPY . /app

RUN mkdir -p /log && \
    mkdir -p /var/tmp/uwsgi_flask_metrics && \
    touch /log/application.log && \
    touch /tmp/reload_uwsgi && \
    touch /tmp/log_uwsgi.log
# 5050 gets connected to the reverse proxy in EB
EXPOSE 5050
ENV PYTHONPATH=. 

CMD [ "uwsgi", "--ini=uwsgi.ini" ]
# *** END service-specific customizations
