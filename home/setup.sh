#!/bin/bash
set -e

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y libusb-1.0-0-dev make unzip wget

cd $HOME

wget -N https://bit-trade-one.co.jp/wp/wp-content/uploads/mydownloads/bto_advanced_USBIR_cmd101.zip
rm -rf bto_advanced_USBIR_cmd-1.0.1
unzip bto_advanced_USBIR_cmd101.zip
cd bto_advanced_USBIR_cmd-1.0.1

# bto_advanced_USBIR_cmd.c の libusb_set_debug を libusb_set_option に置換
sed -i 's/libusb_set_debug(ctx, 3);/libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, 3);/' bto_advanced_USBIR_cmd.c

sudo make
sudo make install
mv bto_advanced_USBIR_cmd-1.0.1 $HOME

cd $HOME

echo "Setup Successful!"