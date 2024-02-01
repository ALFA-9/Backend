#!/bin/sh
docker-compose exec web python import_data.py -f post.csv -t post
docker-compose exec web python import_data.py -f grade.csv -t grade
docker-compose exec web python import_data.py -f department.csv -t department
docker-compose exec web python import_data.py -f employee.csv -t employee
