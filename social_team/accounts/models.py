from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class UserAccount(AbstractUser):
    email = models.EmailField('email address', unique=True)
    about_me = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='images/', blank=True)
    skills = models.ManyToManyField(Skill, related_name='user_skills')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
