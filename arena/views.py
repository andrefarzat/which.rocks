from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from .models import Battle, Fighter, Comment, Vote
from django.contrib.auth.models import User
from .forms import BattleForm, VoteForm, FighterForm


# Create your views here.

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
