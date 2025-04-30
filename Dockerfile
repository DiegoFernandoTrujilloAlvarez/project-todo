FROM python:3.13.3-alpine

RUN mkdir -p /home/app

WORKDIR /home/app

COPY . /home/app

# Instalar dependencias del sistema necesarias
RUN apk update && apk upgrade && apk add --virtual build-deps gcc python3-dev postgresql-dev libffi-dev && apk update && apk upgrade

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]