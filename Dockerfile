# syntax=docker/dockerfile:1

FROM python:3.12.7-bookworm

WORKDIR /app
ENV FLASK_APP main.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
