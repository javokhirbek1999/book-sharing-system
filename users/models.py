from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _

from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, email, username, name, password=None, **kwargs):

        if not email:
            raise ValueError(_('Email is required, please enter your email'))
        
        user = self.model(email=self.normalize_email(email), username=username, name=name)

        user.set_password(password)

        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, name, password):

        user = self.create_user(email=email, username=username, name=name, password=password)

        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True, blank=False)
    username = models.CharField(max_length=200, unique=True, blank=False)
    name = models.CharField(max_length=200, blank=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','name']

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }


