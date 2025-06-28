#!/bin/bash
set -e

cd $HOME

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates dphys-swapfile

rm -rf smart-home
git clone https://github.com/Yaaamashiro/smart-home.git

# create swap space
sudo sed -i 's/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile || echo 'CONF_SWAPSIZE=1024' | sudo tee -a /etc/dphys-swapfile

sudo dphys-swapfile setup
sudo dphys-swapfile swapon

echo "✅ swap space created!"

# created .env
cd smart-home

sudo touch .env
sudo chown "$USER":"$USER" .env

global_ip=[$(curl ifconfig.io)]
read -p "DEBUG? (True or False): " debug
read -p "Enter USERNAME: " username
read -s -p "Enter PASSWORD: " password
echo

cat <<EOF > .env
DEBUG=$debug
DJANGO_SECRET_KEY=$password
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=home,$global_ip
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=postgre
DATABASE_USERNAME=$username
DATABASE_PASSWORD=$password
DATABASE_HOST=home-db
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
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo docker compose up home-db home-app --build -d

sudo docker compose exec home-app python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username = '$username';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, '', '$password')
"

echo "✅ docker container built!"

echo "💯 Successful setup!"

rm "$0"