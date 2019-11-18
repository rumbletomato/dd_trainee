FROM python:3.7

RUN mkdir -p /usr/src/simple_crud
WORKDIR /usr/src/simple_crud

COPY requirements.txt /usr/src/simple_crud
RUN pip install -U -r requirements.txt

COPY . /usr/src/simple_crud
