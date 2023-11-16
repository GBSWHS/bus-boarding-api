FROM python:3.9 as dependencies

RUN pip install poetry==1.4.2

COPY . /app/

WORKDIR /app

RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --only main --no-cache


FROM gcr.io/distroless/python3

COPY --from=dependencies /usr/local/lib/python3.9/ /usr/local/lib/python3.9/

COPY . /app/
WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages

ENTRYPOINT ["python", "-m", "bus_boarding_api"]
