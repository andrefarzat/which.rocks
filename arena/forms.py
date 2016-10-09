from django import forms
from django.utils.text import slugify

from arena.models import Battle, Vote, Fighter, Comment

import pdb


class BattleForm(forms.Form):

    def battle_exists(self):
        sql = Battle.objects.filter(fighter_one=self.data['fighter_one'], fighter_two=self.data['fighter_two']) | Battle.objects.filter(fighter_one=self.data['fighter_two'], fighter_two=self.data['fighter_one'])
        if sql.count() == 0:
            return False
        else:
            return True

    class Meta:
        model = Vote
        fields = ('fighter_one', 'fighter_two')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fighter', 'battle')


class FighterForm(forms.ModelForm):

    def clean(self, prefix=None):
        pdb.set_trace()
        if prefix == None:
            if self.data['slug'] == None:
                return False
            else:
                return True
        else:
            if self.data[prefix + '-slug'] == None:
                return False
            else:
                return True

    def save(self):
        instance = super(FighterForm, self).save(commit=False)
        instance.slug = slugify(instance.name)
        instance.save()
        return instance

    class Meta:
        model = Fighter
        fields = ('name', 'description', 'image', 'slug')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('battle', 'fighter', 'description')
