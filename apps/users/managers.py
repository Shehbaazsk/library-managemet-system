from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have Email address")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email.lower()), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
