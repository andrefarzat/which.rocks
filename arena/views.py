from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import *
from .forms import VoteForm


# Create your views here.

def hello(request):
    return HttpResponse("Hello world")


def index(request):
    return HttpResponse("Hello, world. You're at the battle index.")


def battle(request, fighter_one, fighter_two):
    try:
        battle = Battle.objects.get(fighter_one=Fighter.objects.get(name=fighter_one), fighter_two=Fighter.objects.get(name=fighter_two))
    except:
        try:
            battle = Battle.objects.get(fighter_one=Fighter.objects.get(name=fighter_two), fighter_two=Fighter.objects.get(name=fighter_one))
        except:
            return HttpResponseNotFound('Battle not found')

    latest_comment_fighter_one = Comment.objects.filter(fighter=battle.fighter_one).order_by('date_created')[:5]
    latest_comment_fighter_two = Comment.objects.filter(fighter=battle.fighter_two).order_by('date_created')[:5]

    return render(request, 'battle.html', {'battle': battle, 'latest_comment_fighter_one': latest_comment_fighter_one, 'latest_comment_fighter_two': latest_comment_fighter_two,})
