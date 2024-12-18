from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.models import Author, User
from apps.utils.common_model import CommonModelSerializer
from apps.utils.exceptions import CustomValidationError


class AuthorRegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(
        write_only=True, required=True, label="Password Confirmation"
    )
    bio = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "password2",
                  "bio", "first_name"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise CustomValidationError(
                "A user with this email already exists."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise CustomValidationError("The password field does not match")
        del attrs["password2"]

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class ListAuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ["user", "bio"]


class UserAllDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)


class GetAuthorSerializer(serializers.ModelSerializer):
    user = UserAllDetailsSerializer()

    class Meta():
        model = Author
        fields = ["user", "bio"]
