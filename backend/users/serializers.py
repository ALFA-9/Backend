import random

from rest_framework import serializers

from .models import Employee
from .constants import HARD_SKILLS, SOFT_SKILLS


class SkillsMixin:
    hard_skills = serializers.SerializerMethodField()
    soft_skills = serializers.SerializerMethodField()

    def get_hard_skills(self):
        hard_skills = dict()
        score = 0
        for skill in HARD_SKILLS:
            hard_skills[skill] = random.randint(1,11)
            score += hard_skills[skill]
        hard_skills["average"] = score / len(HARD_SKILLS)
        return hard_skills
    
    def get_soft_skills(self):
        soft_skills = dict()
        score = 0
        for skill in SOFT_SKILLS:
            soft_skills[skill] = random.randint(1,11)
            score += soft_skills[skill]
        soft_skills["average"] = score / len(SOFT_SKILLS)
        return soft_skills


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmployeeSerializer(SkillsMixin, serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""
    idps = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()

    def get_idps(self, user):
        return user.idp_employee
    
    def get_directors(self, user):
        return Employee.get_ancestors(ascending=False, include_self=False)

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "grade",
            "post",
            "department",
            "is_staff",
            "image",
            "hard_skills",
            "soft_skills",
        )


class DirectorSerializer(EmployeeSerializer):
    """Сериализатор для кастомной модели пользователя."""

    subordinates = serializers.SerializerMethodField()

    def __init__(self, *kwrgs, max_depth):
        self.max_depth = max_depth
        super().__init__(*kwrgs)

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "grade",
            "post",
            "department",
            "subordinates",
            "is_staff",
        )

    def get_subordinates(self, director):
        if self.max_depth > 1:
            serializer = DirectorSerializer(
                director.get_descendants(include_self=False).filter(
                    level__lte=director.level + self.max_depth
                ),
                max_depth=self.max_depth - 1,
                many=True,
            )
            return serializer.data
