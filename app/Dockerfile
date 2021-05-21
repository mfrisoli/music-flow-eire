FROM python:3.8

LABEL maintainer "Marco F"

RUN apt-get update

COPY ./ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run"]
