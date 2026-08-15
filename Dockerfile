# Используем официальный образ Python с поддержкой звука
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    alsa-utils \
    libasound2-dev \
    build-essential \
    python3-dev \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Официальный PyPI (files.pythonhosted.org) отдаёт из РФ/СНГ на единицы КБ/с — зеркало Aliyun на порядок быстрее
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY src/ ./src/

COPY models/ ./models/

CMD ["python", "src/main.py"]