docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Add is_active to User table"
docker-compose run backend alembic upgrade head