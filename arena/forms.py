import itertools

from arena.models import Battle, Vote, Fighter, Comment

from django import forms
from django.utils.text import slugify


class FighterForm(forms.ModelForm):
    slug = forms.CharField(required=False)

    def save(self):
        instance = super(FighterForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.name)
        for x in itertools.count(1):
            if not Fighter.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s_%d' % (orig, x)
        instance.save()
        return instance

    class Meta:
        model = Fighter
        fields = ('name', 'description', 'image', 'slug')


class BattleForm(forms.ModelForm):

    def exists(self):
        fighter_one = Fighter.objects.get(id=self.data['fighter_one'])
        fighter_two = Fighter.objects.get(id=self.data['fighter_two'])
        sql = Battle.objects.filter(fighter_one=fighter_one, fighter_two=fighter_two) | Battle.objects.filter(fighter_one=fighter_two, fighter_two=fighter_one)
        if sql.count() == 0:
            return False
        else:
            return True

    def save(self):
        instance = super(BattleForm, self).save(commit=False)
        instance.save()
        return instance

    class Meta:
        model = Battle
        fields = ('fighter_one', 'fighter_two', 'creator')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fighter', 'battle')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('battle', 'fighter', 'description')
