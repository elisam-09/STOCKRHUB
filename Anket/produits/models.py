from django.db import models

from django.db import models

class Produit(models.Model):
    """Représente un produit ou service vendu par l'entreprise"""
    
    # Informations essentielles 
    reference = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Optionnel
    
    prix_ht = models.DecimalField(max_digits=15, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Stock (optionnel, pour les produits physiques)
    stock_actuel = models.IntegerField(default=0, blank=True)
    stock_mini_alerte = models.IntegerField(default=5, blank=True)
    
    
    def __str__(self):
        return f"{self.reference} - {self.nom}"
    
    @property
    def prix_ttc(self):
        """Calcule le prix TTC automatiquement"""
        return self.prix_ht * (1 + self.taux_tva / 100)
