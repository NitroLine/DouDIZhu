FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV TORNADO_SETTINGS_MODULE settings.production

COPY requirements.txt requirements.txt


RUN apk add --no-cache --virtual .build-deps gcc musl-dev openssl-dev libffi-dev
RUN pip install -U setuptools pip && pip install -r requirements.txt -i https://pypi.douban.com/simple

COPY doudizhu/ /app
WORKDIR /app
EXPOSE 8080
CMD ["python3", "app.py"]
