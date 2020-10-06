FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/

WORKDIR /app/

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "connector.py", "funnel_exec"]
