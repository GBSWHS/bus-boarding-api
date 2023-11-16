FROM alpine

RUN apk add --no-cache python3 py3-pip

RUN pip3 install poetry==1.4.2

COPY . /app/

WORKDIR /app

RUN python3 -m poetry config virtualenvs.create false
RUN python3 -m poetry install --only main --no-cache

CMD ["python3", "-m", "bus_boarding_api"]
