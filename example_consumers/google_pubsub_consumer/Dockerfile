FROM python:3-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/

WORKDIR /data/www/

COPY requirements.txt /data/www/

RUN pip install -r requirements.txt

COPY . /data/www/

CMD ["python", "consumer.py", "customer"]
