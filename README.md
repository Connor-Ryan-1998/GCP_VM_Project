# GCP_VM_Project
Flask application to sit on GCP VM

sudo apt update -y;sudo apt upgrade -y

sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname
-s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get install docker.io -y
sudo apt-get install docker-compose -y

git clone https://github.com/Connor-Ryan-1998/GCP_VM_Project.git && cd GCP_VM_Project

sudo docker-compose -f docker-compose.yml up -d 

# Test/Debug
sudo docker-compose ps
