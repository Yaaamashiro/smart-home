#!/bin/bash
set -e

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates dphys-swapfile

rm -rf smart-home
git clone https://github.com/Yaaamashiro/smart-home.git
cd smart-home/home

# create swap space
sudo sed -i 's/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile || echo 'CONF_SWAPSIZE=1024' | sudo tee -a /etc/dphys-swapfile

sudo dphys-swapfile setup
sudo dphys-swapfile swapon

echo "✅ swap space created!"

# created .env
sudo touch .env
sudo chown "$USER":"$USER" .env
read -p "DEBUG? (True or False): " debug
read -p "Enter USERNAME: " username
read -s -p "Enter PASSWORD: " password
echo

cat <<EOF > .env
DEBUG=$debug
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
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

cd $HOME/smart-home
sudo docker compose up --build -d
sudo docker compose exec home python manage.py migrate --noinput

sudo docker compose exec home python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('$username', '', '$password')
"

echo "✅ docker container built!"

echo "💯 Successful setup!"

rm "$0"