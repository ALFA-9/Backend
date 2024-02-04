#!/bin/sh
docker compose exec web alembic upgrade head
docker compose exec web python import_data.py -f data/post.csv -t post
docker compose exec web python import_data.py -f data/grade.csv -t grade
docker compose exec web python import_data.py -f data/department.csv -t department
docker compose exec web python import_data.py -f data/employee.csv -t employee
docker compose exec web python import_data.py -f data/control.csv -t control
docker compose exec web python import_data.py -f data/type.csv -t type
docker compose exec web python import_data.py -f data/idp.csv -t idp
docker compose exec web python import_data.py -f data/task.csv -t task
docker compose exec web python import_data.py -f data/comment.csv -t comment