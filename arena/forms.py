from django import forms
from .models import Battle, Vote, Fighter


class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('fighter_one', 'fighter_two')

class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fighter','battle')

class FighterForm(forms.ModelForm):

    class Meta:
        model = Fighter
        fields = ('name','description','image')
