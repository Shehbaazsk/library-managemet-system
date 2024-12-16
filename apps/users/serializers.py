from rest_framework import serializers

from apps.users.models import User


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
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "A user with this email already exist")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        del attrs["password2"]

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "email", "first_name", "last_name"]
