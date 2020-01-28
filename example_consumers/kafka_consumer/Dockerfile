FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/

WORKDIR /data/www/

COPY . /data/www/

RUN pip install -r requirements.txt

CMD ["python", "consumer.py", "customer"]
