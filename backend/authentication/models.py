from django.db import models
from django.contrib.auth.models import (

    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin

)
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extrafield):
        user = self.model(email=email, **extrafield)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extrafield):
        user = self.model(email=email, **extrafield)
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
