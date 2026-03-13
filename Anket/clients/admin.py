from django.contrib import admin

from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'telephone_1', 'telephone_2', 'date_ajout']

