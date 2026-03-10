from flask import Blueprint, request, jsonify
from models import db, Sale, Product, token_required
from services.stock_service import StockService
from services.alert_service import AlertService
from datetime import datetime

sale_bp = Blueprint('sale', __name__)

@sale_bp.route('/', methods=['GET'])
@token_required
def get_sales(current_user):
    """Récupère uniquement les ventes de l'utilisateur connecté"""
    sales = Sale.query.filter_by(user_id=current_user.id).order_by(Sale.timestamp.desc()).limit(100).all()
    return jsonify([s.to_dict() for s in sales])

@sale_bp.route('/', methods=['POST'])
@token_required
def create_sale(current_user):
    """Crée une vente pour l'utilisateur connecté"""
    data = request.json
    
    product = Product.query.filter_by(id=data['product_id'], user_id=current_user.id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    quantity = data.get('quantity', 1)
    
    # Consume articles (à modifier pour prendre en compte user_id)
    alerts_generated = StockService.consume_articles_for_sale(product.id, quantity, current_user.id)
    
    if alerts_generated is False:
        return jsonify({'error': 'Not enough stock'}), 400
    
    # Crée la vente avec l'utilisateur
    sale = Sale(
        product_id=product.id,
        quantity=quantity,
        user_id=current_user.id  # ← LIAISON IMPORTANTE
    )
    
    db.session.add(sale)
    db.session.commit()
    
    # Récupère les alertes pour cet utilisateur
    all_alerts = AlertService.get_user_alerts(current_user.id)
    
    return jsonify({
        'sale': sale.to_dict(),
        'alerts': alerts_generated or [],
        'all_alerts': all_alerts
    }), 201
    

