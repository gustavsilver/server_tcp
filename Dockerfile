FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY server.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 22222

CMD ["python", "-u", "server.py"]
