FROM python:3.13.0-alpine3.20

WORKDIR /green-art/fastapi

COPY . .

RUN pip install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]