FROM alpine:3.14
WORKDIR /app
COPY ./src /app/src
COPY ./.cache /app/.cache
COPY ./.env /app/.env

COPY ./requirements.lock /app/requirements.lock
RUN apk add python3 py3-pip && pip install -r /app/requirements.lock && \
    rm /app/requirements.lock


CMD ["python", "/app/src/bot.py"]
