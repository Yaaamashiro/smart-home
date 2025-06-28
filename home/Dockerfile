FROM python:3.12-slim AS builder

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y build-essential libusb-1.0-0-dev unzip wget

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /tmp
RUN wget -N https://bit-trade-one.co.jp/wp/wp-content/uploads/mydownloads/bto_advanced_USBIR_cmd101.zip && \
    unzip bto_advanced_USBIR_cmd101.zip && \
    rm bto_advanced_USBIR_cmd101.zip && \
    cd bto_advanced_USBIR_cmd-1.0.1 && \
    sed -i 's/libusb_set_debug(ctx, 3);/libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, 3);/' bto_advanced_USBIR_cmd.c && \
    make && \
    make install && \
    cd / && rm -rf /tmp/*

FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y libusb-1.0-0

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --chown=appuser:appuser . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "home.wsgi:application"]
