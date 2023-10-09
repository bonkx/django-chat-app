FROM python:3.11-slim

# set environment variables
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg dependencies
## GDAL repository: binutils libproj-dev gdal-bin
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    binutils libproj-dev gdal-bin \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

## Install the "instantclient"
# WORKDIR /opt/oracle
# RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
#     unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
#     cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
#     echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

# setting work directory
WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN pip install --upgrade pip
# RUN pip install wheel && pip install --no-cache-dir -r /app/requirements.txt
# RUN pip install -r /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./dash /app