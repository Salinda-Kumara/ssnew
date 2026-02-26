FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    python3-pil \
    gir1.2-gtk-3.0 \
    gir1.2-gdkpixbuf-2.0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

EXPOSE 6000

CMD ["python3", "screenshare.py", "-p", "6000"]
