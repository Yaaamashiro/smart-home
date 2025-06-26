#!/bin/bash
set -e

cd $HOME

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential ca-certificates libusb-1.0-0-dev make unzip wget

# install bto_advanced_USBIR_cmd
wget -N https://bit-trade-one.co.jp/wp/wp-content/uploads/mydownloads/bto_advanced_USBIR_cmd101.zip
rm -rf bto_advanced_USBIR_cmd-1.0.1
unzip bto_advanced_USBIR_cmd101.zip
rm bto_advanced_USBIR_cmd101.zip
cd bto_advanced_USBIR_cmd-1.0.1

sed -i 's/libusb_set_debug(ctx, 3);/libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, 3);/' bto_advanced_USBIR_cmd.c

sudo make
sudo make install

echo "✅ bto_advanced_USBIR_cmd installed!"

cd $HOME

# created .env
sudo touch .env
sudo chown "$USER":"$USER" .env
read -p "Enter USERNAME: " username
read -s -p "Enter PASSWORD: " password
echo

cat <<EOF > .env
DEBUG=False
DJANGO_SECRET_KEY=$password
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=home
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=postgre
DATABASE_USERNAME=$username
DATABASE_PASSWORD=$password
DATABASE_HOST=db
DATABASE_PORT=5432
EOF

echo "✅ .env created!"

# build docker container
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

rm -rf smart-home
git clone https://github.com/Yaaamashiro/smart-home.git
mv smart-home/home/* $HOME
rm -rf smart-home

sudo docker compose up --build -d
sudo docker compose exec django python manage.py migrate --noinput
sudo docker compose exec django python manage.py collectstatic --noinput

sudo docker compose exec django python manage.py shell -c "
  from django.contrib.auth import get_user_model;
  User = get_user_model();
  User.objects.create_superuser('$username', '', '$password')
"

echo "✅ docker container built!"

echo "✅ Successful setup!"

rm "$0"