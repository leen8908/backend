docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Add MR_Rcmed_Member table"
docker-compose run backend alembic upgrade head