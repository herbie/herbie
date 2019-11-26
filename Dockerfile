FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/

WORKDIR /data/www/

COPY . /data/www/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000