FROM python:3.10-slim

# tools
RUN apt-get update -y  \
    && apt-get -y install --no-install-recommends  \
    procps \
    net-tools \
    iputils-ping \
    dnsutils \
    traceroute \
    telnet \
    zlib1g \
    libjpeg-dev \
    libwebp-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libraqm0 \
    libmagic-dev \
    libopenjp2-7-dev \
    liblcms2-dev \
    gcc \
    git \
    curl \
    vim \
    pkg-config \
    libcairo2-dev

# dependencies
COPY requirements.txt requirements.txt
RUN git config --global http.sslverify "false" && pip install --no-cache-dir -r requirements.txt

# application
WORKDIR /app
COPY . /app

# cleanup
RUN apt-get remove -y build-essential gcc python3-dev git \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/