#!/bin/sh
python manage.py csvimport -f data/post.csv -m post
python manage.py csvimport -f data/grade.csv -m grade
python manage.py csvimport -f data/department.csv -m department
python manage.py csvimport -f data/employee.csv -m employee
python manage.py csvimport -f data/control.csv -m taskcontrol
python manage.py csvimport -f data/type.csv -m tasktype
python manage.py csvimport -f data/idp.csv -m idp
python manage.py csvimport -f data/task.csv -m task
python manage.py csvimport -f data/comment.csv -m comment