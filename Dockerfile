FROM alpine:3.14
WORKDIR /app
COPY ./src /app/src
COPY ./.cache /app/.cache
COPY ./.env /app/.env

COPY ./requirements.txt /app/requirements.txt
RUN apk add python3 py3-pip && \
    pip install -r /app/requirements.txt && \
    rm /app/requirements.txt

CMD ["python", "/app/src/bot.py"]
