FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN python3 -m pip install google
RUN python3 -m pip install protobuf
ADD . /code/
