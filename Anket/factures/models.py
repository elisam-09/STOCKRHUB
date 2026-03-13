from django.db import models

from django.contrib.auth.models import User
from clients.models import Client
from produits.models import Produit

class Facture(models.Model):
    """Représente une facture ou un devis"""
    
    # Types de document
    TYPE_CHOICES = [
        ('DEVIS', 'Devis'),
        ('FACTURE', 'Facture'),
        ('AVOIR', 'Avoir'),
    ]
    
    # Statuts
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('ENVOYE', 'Envoyé'),
        ('PAYE', 'Payé'),
        ('EN_RETARD', 'En retard'),
        ('ANNULE', 'Annulé'),
    ]
    
    # Informations de base
    numero = models.CharField(max_length=20, unique=True)
    type_document = models.CharField(max_length=10, choices=TYPE_CHOICES, default='FACTURE')
    
    # Liens
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Dates
    date_creation = models.DateField(auto_now_add=True)
    date_echeance = models.DateField()
    date_envoi = models.DateField(null=True, blank=True)
    
    # Montants (seront calculés automatiquement)
    total_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Statut
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='BROUILLON')
    
    # Notes
    conditions_paiement = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.numero} - {self.client.nom}"
    
    def save(self, *args, **kwargs):
        # Génération automatique du numéro si non défini
        if not self.numero:
            from datetime import datetime
            annee = datetime.now().year
            # Compte les factures de l'année
            count = Facture.objects.filter(
                type_document=self.type_document,
                date_creation__year=annee
            ).count() + 1
            # Format: FAC-2024-001
            self.numero = f"{self.type_document[:3]}-{annee}-{count:03d}"
        super().save(*args, **kwargs)

class LigneFacture(models.Model):
    """Une ligne de détail dans une facture"""
    
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    
    description = models.CharField(max_length=500)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.facture.numero} - {self.produit.nom}"
    
    @property
    def total_ht(self):
        return self.quantite * self.prix_unitaire_ht
    
    @property
    def total_ttc(self):
        return self.total_ht * (1 + self.taux_tva / 100)
    
    @property
    def recalculer_totaux(self):
        total_ht = 0
        total_tva = 0
    
        for ligne in self.lignes.all():
            ht = ligne.quantite * ligne.prix_unitaire_ht
            tva = ht * ligne.taux_tva / 100
        
            total_ht += ht
            total_tva += tva

        self.total_ht = total_ht
        self.total_tva = total_tva
    
    @property
    def recalculer_totaux(self):
        total_ht = 0
        total_tva = 0
    
        for ligne in self.lignes.all():
            ht = ligne.quantite * ligne.prix_unitaire_ht
            tva = ht * ligne.taux_tva / 100
        
            total_ht += ht
            total_tva += tva

        self.total_ht = total_ht
        self.total_tva = total_tva
        self.total_ttc = total_ht + total_tva
        self.total_ttc = total_ht + total_tva
