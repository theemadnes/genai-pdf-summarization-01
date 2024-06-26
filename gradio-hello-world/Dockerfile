FROM python:3.12.4-slim

#MAINTAINER Alex Mattson "alex.mattson@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app.py /app/app.py

RUN addgroup --system appuser && adduser --system appuser --ingroup appuser
USER appuser

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]