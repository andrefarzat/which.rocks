from django import forms
from .models import Battle, Vote, Fighter, Comment


class BattleForm(forms.Form):
    fighter_one_name = forms.CharField(required=True)
    fighter_one_image = forms.ImageField(required=False)
    fighter_one_description = forms.CharField(required=False)
    fighter_two_name = forms.CharField(required=True)
    fighter_two_image = forms.ImageField(required=False)
    fighter_two_description = forms.CharField(required=False)

    def clean(self):
        data = super().clean()
        raise NotImplemented('Terminar isso aqui')

    def save(self):
        raise NotImplemented('Salvar a batalha aqui')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fighter', 'battle')


class FighterForm(forms.ModelForm):

    class Meta:
        model = Fighter
        fields = ('name', 'description', 'image')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('battle', 'fighter', 'description')
