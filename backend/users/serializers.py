import random

from rest_framework import serializers

from .models import Employee
from .constants import HARD_SKILLS, SOFT_SKILLS
from idps.serializers import IdpSerializer


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ShortDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
        )


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""
    idps = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    hard_skills = serializers.SerializerMethodField()
    soft_skills = serializers.SerializerMethodField()

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
            "directors",
            "is_director",
            "idps",
        )

    def get_hard_skills(self, obj):
        hard_skills = dict()
        score = 0
        for skill in HARD_SKILLS:
            hard_skills[skill] = random.randint(1, 10)
            score += hard_skills[skill]
        hard_skills["average"] = score / len(HARD_SKILLS)
        return hard_skills

    def get_soft_skills(self, obj):
        soft_skills = dict()
        score = 0
        for skill in SOFT_SKILLS:
            soft_skills[skill] = random.randint(1, 10)
            score += soft_skills[skill]
        soft_skills["average"] = score / len(SOFT_SKILLS)
        return soft_skills

    def get_idps(self, user):
        return IdpSerializer(user.idp_employee.first()).data

    def get_directors(self, user):
        return ShortDirectorSerializer(user.get_ancestors(
            ascending=False, include_self=False), many=True).data


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
