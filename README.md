# Stock-WebApp-Docker
Flask web application to sit on GCP VM utilising docker 


### Installation
1. Ensure ubuntu is up to date
`
sudo apt update -y;sudo apt upgrade -y
`
`
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
 
sudo apt-get install docker.io docker-compose  -y
`

### Pull latest web app
`
git clone https://github.com/Connor-Ryan-1998/Stock-WebApp-Docker.git && cd Stock-WebApp-Docker

sudo docker-compose build
sudo docker-compose -f docker-compose.yml up -d 
 `

### Test/Debug
General Debugging
`
sudo docker-compose ps
sudo docker-compose logs
`

Look into containers
`
sudo docker exec -it gcp_vm_project_postgres_1 bash
psql -h localhost -p 5432 -U postgres1 -d production
 `
### Clean Docker
` 
sudo docker-compose down
sudo docker system prune -a 
`

