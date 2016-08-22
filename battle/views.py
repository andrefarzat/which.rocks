from django.views.generic import TemplateView

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

class Battle(TemplateView):
    template_name = "battle.html"

class NewBattle(TemplateView):
    template_name = "new_battle.html"

class Profile(TemplateView):
    template_name = "profile.html"
