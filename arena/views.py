from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Battle, Fighter, Comment
from .forms import VoteForm


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


def new_battle(request):
    return render(request, 'new_battle.html', {})


def fighter_profile(request, fighter_name):
    try:
        fighter = get_object_or_404(Fighter, name=fighter_name)
        latest_comments = Comment.objects.filter(fighter=fighter)
    except:
        pass
    return render(request, 'fighter_profile.html', {'latest_comments': latest_comments,})


def user_profile(request):
    return render(request, 'user_profile.html', {})
