FROM python:3.6-slim

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/usr/src/app/rabbitmq_consumer.py"]
