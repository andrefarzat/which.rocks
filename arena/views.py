from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View

from .models import Battle, Fighter, Comment, Vote
from .forms import BattleForm, VoteForm, FighterForm, CommentForm


# Create your views here.


class VoteView(View):
    template_name = 'vote_new.html'

    def post(self, request):
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
                fighter = Fighter.objects.get(id=request.POST['fighter'])
                return HttpResponse("You voted for " + fighter.name)

    def get(self, request, id=None):
        if id == None :
            form = VoteForm()
            return render(request, self.template_name, {'form': form, })
        else:
            vote = Vote.objects.get(id=id)
            if self.template_name == 'vote_edit.html' :
                form = VoteForm(initial={'battle': Battle.objects.get(id=vote.battle.id), 'fighter': vote.fighter})
                form.fields['battle'].queryset = Battle.objects.filter(id=vote.battle.id)
                form.fields['fighter'].queryset = Fighter.objects.filter(id=vote.battle.fighter_one.id) | Fighter.objects.filter(id=vote.battle.fighter_two.id)
                form.fields['battle'].disabled = True
                return render(request, self.template_name, {'form': form, })
            else:
                return HttpResponse("Vote for " + vote.fighter.name + " in battle " + str(vote.battle.id))

    def put(self, request):
        form = VoteForm(request.PUT)
        changedvote = Vote.objects.get(voter=request.user, battle=Battle.objects.get(id=request.PUT['battle']))
        changedvote.fighter = Fighter.objects.get(id=request.PUT['fighter'])
        changedvote.save()
        return HttpResponse("You changed your vote to " + changedvote.fighter.name)

    def delete(self, request):
        pass    #FIXME


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
