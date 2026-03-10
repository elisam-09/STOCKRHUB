from flask import Blueprint, jsonify
from models import Article, Product



alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/', methods=['GET'])
def get_alerts():
    alerts = []
    
    # Check articles below threshold
    articles = Article.query.all()
    for article in articles:
        if article.is_below_threshold():
            message = f"Il te reste {article.quantity:.1f} {article.unit} de {article.name} — pense à recommander bientôt."
            alerts.append({
                'type': 'stock_low',
                'article_name': article.name,
                'message': message
            })
    
    # Check products with zero producible quantity
    products = Product.query.all()
    for product in products:
        if product.producible_quantity() == 0 and product.composition:
            alerts.append({
                'type': 'product_unavailable',
                'product_name': product.name,
                'message': f"Tu ne peux plus fabriquer {product.name} — vérifie le stock"
            })
    
    return jsonify({
        'count': len(alerts),
        'alerts': alerts
    })