FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
 && pip install .

ENV PYTHONPATH=/app/src
ENV FLASK_APP=src/app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
