FROM ccr.ccs.tencentyun.com/andromeda/tcloud_python:3.7

WORKDIR /tcloud
RUN mkdir logs
COPY . .
CMD ./start.sh
