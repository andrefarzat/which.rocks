from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Fighter(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey('auth.User', related_name='fighters')
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name

    @property
    def battles(self):
        sql = models.Q(fighter_one=self) | models.Q(fighter_two=self)
        return Battle.objects.filter(sql)


class Battle(models.Model):
    creator = models.ForeignKey('auth.User')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    fighter_one = models.ForeignKey(Fighter, related_name='battle_one+')
    fighter_two = models.ForeignKey(Fighter, related_name='battle_two+')

    def __str__(self):
        return str(self.id)


class Vote(models.Model):
    battle = models.ForeignKey(Battle, null=False, blank=False)
    figther = models.ForeignKey(Fighter, null=False, blank=False)
    voter = models.ForeignKey('auth.User')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Comment(models.Model):
    battle = models.ForeignKey(Battle, null=False, blank=False)
    creator = models.ForeignKey('auth.User')
    figther = models.ForeignKey(Fighter, null=False, blank=False)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
