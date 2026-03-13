from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_clients, name='liste'), # Page d'accueil des clients
    path('ajouter/', views.ajouter_client, name='ajouter'), # Ligne ajoutée
]