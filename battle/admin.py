from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Fighter)
admin.site.register(Battle)
admin.site.register(Vote)
admin.site.register(Comment)
