FROM cgr.dev/chainguard/python:latest-dev as dev
#FROM python:3.12.4-slim

#MAINTAINER Alex Mattson "alex.mattson@gmail.com"

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin":$PATH

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

FROM cgr.dev/chainguard/python:latest

COPY app.py app.py
COPY --from=dev /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]