from django.http import HttpResponse
from django.shortcuts import render
from .models import *


# Create your views here.

def hello(request):
    return HttpResponse("Hello world")


def index(request):
    return HttpResponse("Hello, world. You're at the battle index.")


def battle(request, battle_id):
    battle = Battle.objects.get(id=battle_id)
    latest_comment_fighter_one = Comment.objects.filter(figther=battle.fighter_one).order_by('date_created')[:5]
    latest_comment_fighter_two = Comment.objects.filter(figther=battle.fighter_two).order_by('date_created')[:5]
    return render(request, 'battle.html', {'battle': battle, 'latest_comment_fighter_one': latest_comment_fighter_one, 'latest_comment_fighter_two': latest_comment_fighter_two})
