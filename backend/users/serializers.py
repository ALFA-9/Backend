import random

from rest_framework import serializers

from alpha_project.constants import HARD_SKILLS, SOFT_SKILLS
from idps.serializers import IdpWithCurrentTaskSerializer
from users.models import Employee


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

    idps = IdpWithCurrentTaskSerializer(many=True, source="idp_employee")
    hard_skills = serializers.SerializerMethodField()
    soft_skills = serializers.SerializerMethodField()
    is_director = serializers.SerializerMethodField()
    grade = serializers.StringRelatedField()
    post = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "grade",
            "post",
            "department",
            "image",
            "hard_skills",
            "soft_skills",
            "is_director",
            "idps",
        )

    def get_image(self, obj):
        return obj.image.url

    def get_is_director(self, obj) -> bool:
        return not obj.is_leaf_node()

    def get_hard_skills(self, obj) -> dict[str, int]:
        hard_skills = dict()
        score = 0
        for skill in HARD_SKILLS:
            hard_skills[skill] = random.randint(1, 10)
            score += hard_skills[skill]
        hard_skills["average"] = score / len(HARD_SKILLS)
        return hard_skills

    def get_soft_skills(self, obj) -> dict[str, int]:
        soft_skills = dict()
        score = 0
        for skill in SOFT_SKILLS:
            soft_skills[skill] = random.randint(1, 10)
            score += soft_skills[skill]
        soft_skills["average"] = score / len(SOFT_SKILLS)
        return soft_skills


class EmployeeForDirectorSerializer(EmployeeSerializer):
    """Сериализатор для кастомной модели пользователя."""

    status_idp = serializers.SerializerMethodField()
    subordinates = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def __init__(self, *kwrgs, max_depth):
        self.max_depth = max_depth
        super().__init__(*kwrgs)

    class Meta:
        model = Employee
        fields = (
            "id",
            "director",
            "first_name",
            "last_name",
            "patronymic",
            "image",
            "post",
            "status_idp",
            "subordinates",
        )

    def get_image(self, obj):
        return obj.image.url

    def get_status_idp(self, obj) -> str | None:
        last_idp = obj.idp_employee.order_by("-date_start").first()
        if last_idp:
            return last_idp.status_idp
        return

    def get_subordinates(self, director) -> list[dict]:
        if self.max_depth > 1:
            serializer = EmployeeForDirectorSerializer(
                director.get_descendants(include_self=False).filter(
                    level__lte=director.level + self.max_depth
                ),
                max_depth=self.max_depth - 1,
                many=True,
            )
            return serializer.data


class DirectorForEmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""

    name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "name")

    def get_name(self, obj):
        return obj.get_full_name()


class EmployeeWithIdpStatus(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""

    status_idp = serializers.SerializerMethodField()
    post = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "director",
            "first_name",
            "last_name",
            "patronymic",
            "image",
            "post",
            "status_idp",
        )

    def get_image(self, obj):
        return obj.image.url

    def get_status_idp(self, obj) -> str | None:
        last_idp = obj.idp_employee.order_by("-date_start").first()
        if last_idp:
            return last_idp.status_idp
        return
