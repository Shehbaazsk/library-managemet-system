from rest_framework import serializers

from apps.users.models import Author, User


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
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "The password field does not match")
        del attrs["password2"]

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name",]


class ListAuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ["user", "bio"]


class UserAllDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password', 'last_login', 'is_superuser',
                   'is_staff',   'groups', 'user_permissions', 'is_delete')

    def validate_email(self, value):
        """
        Check if the email already exists for a different user
        """
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value


class GetAuthorSerializer(serializers.ModelSerializer):
    user = UserAllDetailsSerializer()

    class Meta():
        model = Author
        fields = ["user", "bio"]

    def validate(self, data):
        print("validaring data", data)
        user_data = data.get('user', {})
        user_instance = self.instance.user if self.instance else None

        user_serializer = UserAllDetailsSerializer(
            instance=user_instance,
            data=user_data,
            context=self.context
        )
        user_serializer.is_valid(raise_exception=True)
        return data
