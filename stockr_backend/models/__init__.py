from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import request, jsonify
from datetime import datetime

db = SQLAlchemy()

# 1. D'abord les modèles de base
from .user import User
from .article import Article

# 2. La table d'association pour les recettes
product_articles = db.Table('product_articles',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('quantity_used', db.Float, nullable=False, default=1.0)
)

# 3. Ensuite les modèles dépendants
from .product import Product
from .sale import Sale
from .scan import InventoryScan # 🔴 AJOUT DE SPECTRA ICI

# -----------------------------------
# DÉCORATEUR D'AUTH (Sécurisé)
# -----------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Accès refusé. Token manquant.'}), 401
        
        user = User.query.filter_by(auth_token=token).first()
        
        if not user:
            return jsonify({'error': 'Token invalide.'}), 401
        
        if user.token_expiry and user.token_expiry < datetime.utcnow():
            return jsonify({'error': 'Session expirée. Veuillez vous reconnecter.'}), 401
        
        return f(user, *args, **kwargs)
    
    return decorated
