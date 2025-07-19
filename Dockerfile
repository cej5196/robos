FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libgl1-mesa-glx chromium-driver && \
    pip install --no-cache-dir -r requirements.txt

ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata"
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
