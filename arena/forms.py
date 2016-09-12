from django import forms
from .models import Battle


class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('fighter_one', 'fighter_two')
