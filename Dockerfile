FROM python:3

#ARG SSH_PRIVATE_KEY

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/

# For now all dependencies in the requirements.txt are public and we don't need an ssh-key.
#RUN mkdir /root/.ssh/
#RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
#RUN chmod 600 /root/.ssh/id_rsa

## Add Github to known hosts
#RUN touch /root/.ssh/known_hosts
#RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

WORKDIR /data/www/

COPY . /data/www/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

