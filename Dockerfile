FROM python:3.11-slim

LABEL org.opencontainers.image.source https://github.com/tanyaestici/nomorevoices

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -Ur requirements.txt && \
    rm requirements.txt

COPY app app

ENTRYPOINT ["python", "-OO", "-m", "app.main"]
