FROM python:3.9

ENV PYTHONUNBUFFERED 1

ENV DOCKERIZE_VERSION v0.6.1

WORKDIR /app

RUN pip install poetry

COPY poetry.lock /app

COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && poetry install --no-root

RUN apt-get update && apt-get install -y wget

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . .

EXPOSE 8000

CMD ["gunicorn", \
     "--workers=2",\
     "--worker-class=gthread",  \
     "--worker-tmp-dir=/dev/shm",\
     "--threads=4", \
     "--log-file=-", \
     "--bind=0.0.0.0:8000",\
     "src.wsgi"]
