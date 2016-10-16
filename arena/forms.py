import itertools

from django import forms
from django.utils.text import slugify

from arena.models import Battle, Vote, Fighter, Comment


class BattleForm(forms.Form):

    def exists(self):
        sql = Battle.objects.filter(fighter_one=self.data['fighter_one'], fighter_two=self.data['fighter_two']) | Battle.objects.filter(fighter_one=self.data['fighter_two'], fighter_two=self.data['fighter_one'])
        if sql.count() == 0:
            return False
        else:
            return True

    def save(self):
        new_battle = Battle(fighter_one=self.data['fighter_one'], fighter_two=self.data['fighter_two'], creator=self.data['creator'])
        new_battle.save()

    class Meta:
        model = Battle
        fields = ('fighter_one', 'fighter_two', 'creator')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fighter', 'battle')


class FighterForm(forms.ModelForm):
    slug = forms.CharField(required=False)

    def save(self):
        instance = super(FighterForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.name)
        for x in itertools.count(1):
            if not Fighter.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        return instance

    class Meta:
        model = Fighter
        fields = ('name', 'description', 'image', 'slug')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('battle', 'fighter', 'description')
