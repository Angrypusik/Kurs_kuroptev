FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Angrypusik/pucik.git .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . /app
WORKDIR /app

# Создаем необходимые директории
RUN mkdir -p /runs/detect/predict

RUN apt-get update && \
    apt-get install -y ffmpeg

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "kurs_kuroptev.py", "--server.port=8501", "--server.address=0.0.0.0"]