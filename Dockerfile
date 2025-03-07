# syntax=docker/dockerfile:1.2
FROM python:3.8.10-slim

WORKDIR /delaymodel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY challenge/model.py /delaymodel
COPY challenge/__init__.py /delaymodel
COPY challenge/api.py /delaymodel
COPY challenge/delay_model.pkl /delaymodel

EXPOSE 8080

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
