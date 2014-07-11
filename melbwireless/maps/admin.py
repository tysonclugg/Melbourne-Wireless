from django.contrib import admin
from django.db.models import get_models
import models

class Member(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_filter = ('applied', 'approved', 'membership_card', 'dob')
    date_hierarchy = 'applied'

class User(admin.ModelAdmin):
    search_fields = ('id', 'name', 'email')
    list_display = ('id', 'name', 'email', 'registered', 'email_confirmed', 'last_seen')
    list_filter = ('registered', 'email_confirmed', 'last_seen', 'failed_attempts', 'adv')

class NodeIp(admin.ModelAdmin):
    list_filter = ('node',)
    list_select_related = True

class Interface(admin.ModelAdmin):
    search_fields = ('mac', 'card_manufacturer')
    list_filter = ('mode', 'class_field')

for model in get_models(models):
    admin.site.register(model, locals().get(model.__name__, None))

