# wallet

# Docker-Compose commands

- https://itsfoss.com/install-docker-arch-linux/
- docker-compose up 
- docker-compose down
- docker-compose up --build

# Docker
- https://itsfoss.com/install-docker-arch-linux/
- docker build . -t wallet
- Waiting
- docker run -p 8000:8000 wallet
- http://127.0.0.1:8000/docs
- docker stop wallet
- docker run -it --rm wallet /bin/bash

### If you need to remove all Docker containers (Dangerous, this will remove all images)

- docker system prune -a

### Or stop all

- docker stop $(docker ps -a -q)

# Alembic

- alembic init migrations
- alembic revision --autogenerate -m "Database creation"
- alembic upgrade head   
