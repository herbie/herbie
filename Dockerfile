FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /data/www/


# create folder structure
RUN mkdir -p /data/www/


# install pg client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# copy and install requirements
COPY requirements.txt /data/www/
RUN pip install -r requirements.txt --upgrade


# copy carl_herbie files
COPY src /data/www/

# setup entrypoint
RUN chmod u+x .docker/entrypoint.sh


ENTRYPOINT [".docker/entrypoint.sh"]

## Using reload to auto-reload when code changes
CMD ["gunicorn", "herbie.wsgi:application", "--bind", "0.0.0.0:80", "--reload"]

