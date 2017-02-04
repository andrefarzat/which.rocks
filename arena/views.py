from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import View
from django import forms

from .models import Battle, Fighter, Comment, Vote
from .forms import BattleForm, VoteForm, FighterForm, CommentForm


class NewView(LoginRequiredMixin, View):
    login_url = 'facebook_login'
    redirect_field_name = '/new/'

    def post(self, request):
        fighters = []
        forms = []
        for prefix in ('one', 'two'):
            form = FighterForm(request.POST, request.FILES, prefix=prefix)
            if form.data[prefix + '-slug'] == '':
                form.instance.creator = request.user
                form.save()
                fighter = form.instance
            else:
                fighter = Fighter.objects.get(slug=request.POST[prefix + '-slug'])
            fighters.append(fighter)
            forms.append(form)

        data = {}
        data['fighter_one'] = fighters[0].id
        data['fighter_two'] = fighters[1].id
        data['creator'] = request.user.id

        battle = BattleForm(data)

        if battle.exists():
            return self.get(request, forms=forms)
        else:
            battle.save()
            return redirect(battle.instance)

    def get(self, request, success=None, forms=None):
        if forms:
            form1 = forms[0]
            form2 = forms[1]
        else:
            form1 = FighterForm(prefix='one')
            form2 = FighterForm(prefix='two')
        #FIXME
        #form1.fields['slug'].widget = forms.HiddenInput()
        #form2.fields['slug'].widget = forms.HiddenInput()
        return render(request, 'new.html', {'fighter1': form1,
                                            'fighter2': form2,
                                            'success': success})

class BattleView(View):
    def get(self, request, slug_one, slug_two):
        try:
            fighter_one = Fighter.objects.get(slug=slug_one)
            fighter_two = Fighter.objects.get(slug=slug_two)
        except Fighter.DoesNotExist:
            return HttpResponse("Fighter doesn't exist")

        battle = Battle.objects.filter(fighter_one=fighter_one, fighter_two=fighter_two) | Battle.objects.filter(fighter_one=fighter_two, fighter_two=fighter_one)

        if battle.count() == 0:
            return HttpResponse("Battle doesn't exist")

        latest_comment_fighter_one = Comment.objects.filter(fighter=battle[0].fighter_one)[:5]
        latest_comment_fighter_two = Comment.objects.filter(fighter=battle[0].fighter_two)[:5]

        return render(request, 'battle.html', { 'battle': battle[0],
                                                'latest_comment_fighter_one': latest_comment_fighter_one,
                                                'latest_comment_fighter_two':latest_comment_fighter_two,})

    def post(self, request, slug_one, slug_two):
        if request.POST['action'] == "vote":
            form = VoteForm(request.POST)
            form.instance.creator = request.user
            form.save()
        if request.POST['action'] == "comment":
            form = CommentForm(request.POST)
            form.instance.creator = request.user
            form.save()
        return self.get(request, slug_one, slug_two)

class HomeView(View):
    def get(self, request):
        battles = Battle.objects.filter()[:20]

        return render(request, 'index.html', {'battles': battles,})


class FighterView(View):
    def get(self, request, fighter_slug):
        fighter = get_object_or_404(Fighter, slug=fighter_slug)
        battles = Battle.objects.filter(fighter_one=fighter) | Battle.objects.filter(fighter_two=fighter)

        return render(request, 'fighter_profile.html', {'battles': battles,})


class UserView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        latest_battles = Battle.objects.filter(creator=user)
        latest_fighters = Fighter.objects.filter(creator=user)
        latest_comments = Comment.objects.filter(creator=user)
        latest_votes = Vote.objects.filter(creator=user)

        return render(request, 'user_profile.html', {'username':username, 'latest_battles':latest_battles, 'latest_fighters':latest_fighters, 'latest_comments':latest_comments, 'latest_votes':latest_votes,})


class SettingsView(View):
    def get(self, request):
        return HttpResponse("Settings page")

#Old stuff
def new_vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            try:
                created = Vote.objects.get(voter = request.user, battle = Battle.objects.get(id=request.POST['battle']))
                return HttpResponse("You already voted in this battle")
            except:
                newvote = Vote(
                    voter = request.user,
                    battle = Battle.objects.get(id=request.POST['battle']),
                    fighter = Fighter.objects.get(id=request.POST['fighter']),
                    )
                newvote.save()
                return render(request, 'new_vote.html', {'fighter': Fighter.objects.get(id=request.POST['fighter']),})
    else:
        return redirect(index)


def new_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            newcomment = Comment(
                creator = request.user,
                fighter = Fighter.objects.get(id=request.POST['fighter']),
                battle = Battle.objects.get(id=request.POST['battle']),
                description = request.POST['description'],
                )
            newcomment.save()
    else:
        return redirect(index)

    return render(request, 'new_comment.html', {'fighter': Fighter.objects.get(id=request.POST['fighter']),})
