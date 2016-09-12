from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from .models import Battle, Fighter, Comment
from django.contrib.auth.models import User
from .forms import BattleForm


# Create your views here.

def index(request):
    try:
        battles = Battle.objects.filter()[:20]
    except:
        pass
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
    try:
        fighter = get_object_or_404(Fighter, name=fighter_name)
        latest_comments = Comment.objects.filter(fighter=fighter)
    except:
        pass
    return render(request, 'fighter_profile.html', {'latest_comments': latest_comments,})


def user_profile(request):
    try:
        latest_battles = Battle.objects.filter(creator=request.user)
        latest_fighters = Fighter.objects.filter(creator=request.user)
        latest_comments = Comment.objects.filter(creator=request.user)
        latest_votes = Vote.objects.filter(voter=request.user)
    except:
        pass
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
