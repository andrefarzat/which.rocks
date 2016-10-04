from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import View

from .models import Battle, Fighter, Comment, Vote
from .forms import BattleForm, VoteForm, FighterForm, CommentForm


# Create your views here.


class NewView(LoginRequiredMixin, View):
    login_url = 'facebook_login'
    redirect_field_name = '/new/'

    def post(self, request):
        fighters = []

        for prefix in ('one', 'two'):
            try:
                fighter = Fighter.objects.get(name=request.POST[prefix + '-name'])
                fighters.append(fighter)
            except Fighter.DoesNotExist:
                form = FighterForm(request.POST, request.FILES, prefix=prefix)
                if not form.is_valid():
                    return self.get(request)
                else:
                    form.instance.creator = request.user
                    form.save()
                    fighter = form.instance
                    fighters.append(fighter)

        #FIXME: Verificar se batalha já existe
        battle = Battle.objects.create(creator=request.user, fighter_one=fighters[0],
                                       fighter_two=fighters[1])

        return self.get(request, success=True)

    def get(self, request, success=None):
        return render(request, 'new.html', {'fighter1': FighterForm(prefix='one'),
                                            'fighter2': FighterForm(prefix='two'),
                                            'success': success})


def index(request):
    battles = Battle.objects.filter()[:20]

    return render(request, 'index.html', {'battles': battles,})


def battle(request, fighter_one, fighter_two):
    try:
        battle = get_object_or_404(Battle, fighter_one__name=fighter_one, fighter_two__name=fighter_two)
    except:
        battle = get_object_or_404(Battle, fighter_one__name=fighter_two, fighter_two__name=fighter_one)

    latest_comment_fighter_one = Comment.objects.filter(fighter=battle.fighter_one)[:5]
    latest_comment_fighter_two = Comment.objects.filter(fighter=battle.fighter_two)[:5]

    return render(request, 'battle.html', {'battle': battle, 'latest_comment_fighter_one': latest_comment_fighter_one, 'latest_comment_fighter_two': latest_comment_fighter_two,})


def fighter_profile(request, fighter_name):
    fighter = get_object_or_404(Fighter, name=fighter_name)
    battles = Battle.objects.filter(fighter_one=fighter) | Battle.objects.filter(fighter_two=fighter)

    return render(request, 'fighter_profile.html', {'battles': battles,})


def user_profile(request):
    latest_battles = Battle.objects.filter(creator=request.user)
    latest_fighters = Fighter.objects.filter(creator=request.user)
    latest_comments = Comment.objects.filter(creator=request.user)
    latest_votes = Vote.objects.filter(voter=request.user)

    return render(request, 'user_profile.html', {'latest_battles':latest_battles, 'latest_fighters':latest_fighters, 'latest_comments':latest_comments, 'latest_votes':latest_votes,})


def new_battle(request):
    if request.method == 'POST':
        form = BattleForm(request.POST)
        if form.is_valid():
            try:
                created = Battle.objects.get(Q(fighter_one=request.POST['fighter_one'], fighter_two=request.POST['fighter_two']) | Q(fighter_one=request.POST['fighter_two'], fighter_two=request.POST['fighter_one']))
                return HttpResponse("This battle already exist")
            except:
                newbattle = Battle(
                    creator = request.user,
                    fighter_one = Fighter.objects.get(id=request.POST['fighter_one']),
                    fighter_two = Fighter.objects.get(id=request.POST['fighter_two']),
                    )
                newbattle.save()
    else:
        form = BattleForm()

    return render(request, 'new_battle.html', {'form': form,})


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


def new_fighter(request):
    if request.method == 'POST':
        form = FighterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                created = Fighter.objects.get(name = request.POST['name'])
                return HttpResponse("This fighter already exist")
            except:
                newfighter = Fighter(
                    name = request.POST['name'],
                    creator = request.user,
                    description = request.POST['description'],
                    image = request.FILES['image'],
                    )
                newfighter.save()
    else:
        form = FighterForm()

    return render(request, 'new_fighter.html', {'form': form,})


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
