FROM python:3.8-alpine

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

WORKDIR /garage

RUN apk add --update --no-cache build-base jpeg-dev zlib-dev \
    postgresql-libs musl-dev postgresql-dev
ENV LIBRARY_PATH=/lib:/usr/lib

COPY requirements.txt /garage/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache -r /garage/requirements.txt

COPY . /garage
CMD sleep 10 && python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
