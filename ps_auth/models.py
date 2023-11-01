
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth import validators as auth_validators


# Create your models here.
class PSUserManager(auth_models.BaseUserManager):

    def create_user(self, username, email, password):

        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have a username")

        if not password:
            raise ValueError("Users must have a password")

        normalized_username = auth_models.AbstractBaseUser.normalize_username(
            username)

        user = self.model(
            username=normalized_username,
            email=self.normalize_email(email),
        )

        # Method belongs to AbstractBaseUser
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(
            username,
            email,
            password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_email(self, email):
        return self.get(**{self.model.EMAIL_FIELD: email})


class PSUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    username = models.CharField(verbose_name="username",
                                max_length=25,
                                unique=True,
                                blank=False,
                                validators=[
                                    auth_validators.UnicodeUsernameValidator],
                                error_messages={
                                    "unique": "A user with that username already exists.",
                                })

    email = models.EmailField(verbose_name="email",
                              max_length=255,
                              unique=True,
                              blank=False,
                              error_messages={
                                  "unique": "A user with that email already exists.",
                              })

    is_active = models.BooleanField(
        verbose_name="active user",
        default=True,
    )

    is_admin = models.BooleanField(
        verbose_name="admin access",
        default=False,
    )

    date_created = models.DateTimeField(auto_now_add=True)

    objects = PSUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self) -> str:
        return self.email


class VerifiedEmail(models.Model):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.email
