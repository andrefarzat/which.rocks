from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse



class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Fighter(BaseModel):
    creator = models.ForeignKey('auth.User', related_name='fighters')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.slug

    @property
    def battles(self):
        sql = models.Q(fighter_one=self) | models.Q(fighter_two=self)
        return Battle.objects.filter(sql)


class Battle(BaseModel):
    creator = models.ForeignKey('auth.User', related_name='battles')
    fighter_one = models.ForeignKey(Fighter, related_name='+')
    fighter_two = models.ForeignKey(Fighter, related_name='+')

    def __str__(self):
        return str(self.id)

    @property
    def fighters(self):
        return Fighter.objects.filter(id__in=[self.fighter_one_id, self.fighter_two_id])

    def get_absolute_url(self):
        return reverse('battle_page', args=(self.fighter_one.slug, self.fighter_two.slug))

    class Meta:
         unique_together = ('fighter_one', 'fighter_two')


class Vote(BaseModel):
    creator = models.ForeignKey('auth.User', related_name='votes')
    battle = models.ForeignKey(Battle, null=False, blank=False)
    fighter = models.ForeignKey(Fighter, null=False, blank=False)

    class Meta:
         unique_together = ('battle', 'creator')


class Comment(BaseModel):
    creator = models.ForeignKey('auth.User', related_name='comments')
    battle = models.ForeignKey(Battle, null=False, blank=False)
    fighter = models.ForeignKey(Fighter, null=False, blank=False)
    description = models.TextField()
