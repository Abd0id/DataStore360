FROM ubuntu:latest
LABEL authors="abd0id"
COPY . /DataStore360
WORKDIR /DataStore360

ENTRYPOINT ["top", "-b"]