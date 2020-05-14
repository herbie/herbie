FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/

WORKDIR /data/www/

### Setup poetry ################################
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock /data/www/
COPY pyproject.toml /data/www/

### Poetry install ##############################
RUN poetry install --no-interaction;

COPY . /data/www/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

