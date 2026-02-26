FROM python:3.11-slim

# Install system dependencies for pyscreenshot and pygdk3 backend
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-gdkpixbuf-2.0 \
    libgirepository1.0-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt PyGObject

COPY . .

EXPOSE 6000

CMD ["python", "screenshare.py", "-p", "6000"]
