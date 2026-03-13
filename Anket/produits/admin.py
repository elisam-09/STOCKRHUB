from django.contrib import admin

from .models import Produit

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['reference', 'nom', 'prix_ht', 'prix_ttc', 'stock_actuel']
    list_filter = ['date_creation']
    search_fields = ['reference', 'nom', 'date_creation']
