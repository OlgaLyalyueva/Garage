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

RUN chmod 755 /garage/start.sh

CMD ["./start.sh"]
EXPOSE 8000
