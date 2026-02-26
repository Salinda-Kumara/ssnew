FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    python3-pil \
    gir1.2-gtk-3.0 \
    gir1.2-gdkpixbuf-2.0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

EXPOSE 6100

CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & sleep 2 && export DISPLAY=:99 && python3 screenshare.py -p 6100"]
