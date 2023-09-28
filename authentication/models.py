from typing import Iterable, Optional
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,AbstractUser
from django.contrib.auth.hashers import make_password

from django.db import models
from django.utils import timezone


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(('You must provide an email address'))
        # convert all in lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', False )
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_user', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, user_name, first_name, password, **other_fields)


class User(AbstractUser):
    user_type= (
        ('Customer', 'Customer'),
        ('Driver', 'Driver')
    )
    phone = models.BigIntegerField(unique=True)
    usertype = models.CharField(choices=user_type, max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['usertype', "username"]

    db_table = "User"

    # def save(self, *args, **kwargs): 
    #      if self.password is not None:   
    #          self.password = self.set_password(self.password)   
    #          return super(User, self).save(*args,*kwargs)

    def __str__(self):
        return str(self.phone)
    


class registeruser(models.Model): 
    name = models.CharField(max_length=100, null=True, blank=True)


    