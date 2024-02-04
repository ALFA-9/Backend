#!/bin/sh
docker compose exec backend python manage.py csvimport -f data/post.csv -m post
docker compose exec backend python manage.py csvimport -f data/grade.csv -m grade
docker compose exec backend python manage.py csvimport -f data/department.csv -m department
docker compose exec backend python manage.py csvimport -f data/employee.csv -m employee
docker compose exec backend python manage.py csvimport -f data/control.csv -m control
docker compose exec backend python manage.py csvimport -f data/type.csv -m type
docker compose exec backend python manage.py csvimport -f data/idp.csv -m idp
docker compose exec backend python manage.py csvimport -f data/task.csv -m task
docker compose exec backend python manage.py csvimport -f data/comment.csv -m comment