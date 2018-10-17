FROM python:3.6.3-slim
RUN apt-get update && apt-get -y install libffi-dev g++ libssl-dev gcc libcairo2-dev git
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/django/django.git
