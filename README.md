# GCP_VM_Project
Flask application to sit on GCP VM


//Ensure ubuntu is up to date
sudo apt update -y;sudo apt upgrade -y


sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get install docker.io docker-compose  -y


///Pull latest web app

git clone https://github.com/Connor-Ryan-1998/GCP_VM_Project.git && cd GCP_VM_Project

sudo docker-compose build
sudo docker-compose -f docker-compose.yml up -d 
 
# Test/Debug
sudo docker-compose ps
sudo docker-compose logs

sudo docker exec -it gcp_vm_project_postgres_1 bash
psql -h localhost -p 5432 -U postgres -d production
 
### wipe images 
docker system prune -a


