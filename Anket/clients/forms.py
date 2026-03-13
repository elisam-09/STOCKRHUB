from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier un client"""
    
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone_1', 'telephone_2']  # Les champs à afficher
        labels = {
            'nom': 'Nom de l\'entreprise ou personne',
            'email': 'Adresse email',
            'telephone_1': 'Numéro de téléphone',
            'telephone_2': 'Numéro de téléphone',
        }