FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

CMD ["sh", "-c", "alembic upgrade head && gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]
