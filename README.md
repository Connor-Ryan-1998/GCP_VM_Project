# GCP_VM_Project
Flask application to sit on GCP VM

sudo apt-get update

sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname
-s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get install docker.io -y
sudo apt-get install docker-compose -y

sudo docker-compose -f docker-compose.yml up -d 