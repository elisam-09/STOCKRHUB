from django.db import models

class Client(models.Model):
    """Un client de mon entreprise"""
    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telephone_1 = models.CharField(max_length=15, blank=True)
    telephone_2 = models.CharField(max_length=15, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom
