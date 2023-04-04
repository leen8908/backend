docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Create Demo 1 database table"
docker-compose run backend alembic upgrade head