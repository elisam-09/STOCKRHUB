from django.shortcuts import render

from .models import Client  # On importe notre modèle Client

def liste_clients(request):
    """Affiche la liste de tous les clients"""
    # Récupère tous les clients depuis la base de données
    tous_les_clients = Client.objects.all()
    
    # Prépare les données à envoyer au template
    contexte = {
        'clients': tous_les_clients,
        'total': tous_les_clients.count()
    }
    
    # Affiche la page avec la liste
    return render(request, 'clients/liste.html', contexte)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from .forms import ClientForm  # ← On importe notre formulaire

# ... (gardez la fonction liste_clients existante)

def ajouter_client(request):
    """Affiche et traite le formulaire d'ajout de client"""
    
    if request.method == 'POST':
        # L'utilisateur a envoyé le formulaire
        form = ClientForm(request.POST)
        if form.is_valid():
            # Sauvegarde dans la base de données
            form.save()
            # Message de succès
            messages.success(request, 'Client ajouté avec succès !')
            # Redirige vers la liste
            return redirect('liste')  # 'liste' est le nom de notre URL
    else:
        # Première visite : formulaire vide
        form = ClientForm()
    
    return render(request, 'clients/ajouter.html', {'form': form})
