FROM alpine
RUN apk add --update --no-cache python3 git && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools build twine pyyaml
WORKDIR /build
# ENTRYPOINT [ "python3 -m build" ]
