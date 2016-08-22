from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    alias = models.ForeignKey('allauth.socialaccount.providers.facebook.username')
    def __str__(self):
        return self.alias.username

class Fighter(models.Model):
    alias = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    def __str__(self):
        return self.alias

class Battle(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    fighters = models.ManyToManyField(Fighter)
    def __str__(self):
        return str(self.id)

class Vote(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    figther = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    figther = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.id)
