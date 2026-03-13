from django.contrib import admin

from django.contrib import admin
from .models import Facture, LigneFacture

class LigneFactureInline(admin.TabularInline):
    """Permet d'éditer les lignes directement dans la facture"""
    model = LigneFacture
    extra = 1  # Nombre de lignes vides à afficher

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'date_creation', 'total_ttc', 'statut', 'type_document']
    list_filter = ['statut', 'type_document', 'date_creation']
    search_fields = ['numero', 'client__nom']
    inlines = [LigneFactureInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('numero', 'type_document', 'client', 'createur')
        }),
        ('Dates', {
            'fields': ('date_echeance', 'date_envoi')
        }),
        ('Montants', {
            'fields': ('total_ht', 'total_tva', 'total_ttc'),
            'classes': ('collapse',)  # Réduit par défaut
        }),
        ('Statut et notes', {
            'fields': ('statut', 'conditions_paiement', 'notes')
        }),
    )

@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ['facture', 'produit', 'quantite', 'total_ht']