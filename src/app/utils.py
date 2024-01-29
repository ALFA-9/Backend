from sqlalchemy import and_, select

from app.database.models import Employee


def get_all_childs_id(parent_id):
    # найти все дочерние элементы
    included = (
        select(Employee.id)
        .where(Employee.director_id == parent_id)
        .cte(name="included", recursive=True)
    )
    # собрать все id этих элементов
    included = included.union_all(
        select(Employee.id).where(Employee.director_id == included.c.id)
    )
    return included


def get_all_parents_id(child_id):
    included = (
        select(Employee.director_id)
        .where(Employee.id == child_id)
        .cte(recursive=True)
    )

    included = included.union_all(
        select(Employee.director_id).filter(
            and_(
                Employee.id == included.c.director_id,
                Employee.director_id.is_not(None),
            )
        )
    )

    return included
