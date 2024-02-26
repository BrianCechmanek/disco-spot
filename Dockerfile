FROM python:3.11-slim
WORKDIR /app
COPY ./src /app/src
COPY ./.cache /app/.cache
COPY ./.env /app/.env

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt && \
    rm /app/requirements.txt

CMD ["python", "/app/src/disco_spot/bot.py"]
