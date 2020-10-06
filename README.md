# GCP_VM_Project
Flask application to sit on GCP VM

sudo apt update -y;sudo apt upgrade -y
sudo apt install software-properties-common

sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname
-s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get install docker.io -y
sudo apt-get install docker-compose -y

git clone https://github.com/Connor-Ryan-1998/GCP_VM_Project.git

sudo docker-compose -f docker-compose.yml up -d 

# Test/Debug
docker-compose ps

## To install python 3.8 for testing before compose
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8 -y

sudo docker build -t a1:latest .

#running docker build 
sudo docker run -p :9090 a1


-- View inside
sudo docker run -it a1 sh 