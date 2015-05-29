FROM ubuntu:14.04
MAINTAINER Jelle Hellemans no@spam.com

RUN apt-get update \
  && apt-get install -y wget python python-pip python-dev libssl-dev libffi-dev bash \
  && apt-get install -y npm \
  && rm -r /var/lib/apt/lists/*
  
RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN npm install -g localtunnel 

# Install Forego
RUN wget -P /usr/local/bin https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego \
 && chmod u+x /usr/local/bin/forego

ENV DOCKER_GEN_VERSION 0.3.9

RUN wget https://github.com/jwilder/docker-gen/releases/download/$DOCKER_GEN_VERSION/docker-gen-linux-amd64-$DOCKER_GEN_VERSION.tar.gz \
 && tar -C /usr/local/bin -xvzf docker-gen-linux-amd64-$DOCKER_GEN_VERSION.tar.gz \
 && rm /docker-gen-linux-amd64-$DOCKER_GEN_VERSION.tar.gz

COPY . /app/
WORKDIR /app/

ENV DOCKER_HOST unix:///tmp/docker.sock

CMD ["forego", "start", "-r"]
