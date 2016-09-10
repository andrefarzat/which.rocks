from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Battle, Fighter, Comment
from .forms import VoteForm


# Create your views here.

def hello(request):
    return HttpResponse("Hello world")


def index(request):
    return HttpResponse("Hello, world. You're at the battle index.")


def battle(request, fighter_one, fighter_two):
    try:
        battle = get_object_or_404(Battle, fighter_one__name=fighter_one, fighter_two__name=fighter_two)
    except:
        battle = get_object_or_404(Battle, fighter_one__name=fighter_two, fighter_two__name=fighter_one)

    latest_comment_fighter_one = Comment.objects.filter(fighter=battle.fighter_one)[:5]
    latest_comment_fighter_two = Comment.objects.filter(fighter=battle.fighter_two)[:5]

    return render(request, 'battle.html', {'battle': battle, 'latest_comment_fighter_one': latest_comment_fighter_one, 'latest_comment_fighter_two': latest_comment_fighter_two,})
