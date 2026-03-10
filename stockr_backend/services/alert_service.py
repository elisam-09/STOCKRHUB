from models import Article, Product

class AlertService:
    
    @staticmethod
    def get_user_alerts(user_id):
        """Generate user-friendly alerts for a specific user"""
        alerts = []
        
        # Check articles below threshold for this user
        articles = Article.query.filter_by(user_id=user_id).all()
        for article in articles:
            if article.is_below_threshold():
                message = f"Il te reste {article.quantity:.1f} {article.unit} de {article.name} — pense à recommander bientôt."
                
                # Get products that use this article (filtered by user)
                products_affected = [p.name for p in article.used_in_products if p.user_id == user_id]
                
                alerts.append({
                    'type': 'stock_low',
                    'article_id': article.id,
                    'article_name': article.name,
                    'quantity': article.quantity,
                    'unit': article.unit,
                    'message': message,
                    'products_affected': products_affected
                })
        
        # Check products with zero producible quantity for this user
        products = Product.query.filter_by(user_id=user_id).all()
        for product in products:
            producible = product.producible_quantity()
            if producible == 0 and product.composition:
                missing_articles = []
                for comp in product.get_composition_details():
                    if comp['article']['quantity'] < comp['quantity_used']:
                        missing_articles.append(comp['article']['name'])
                
                alerts.append({
                    'type': 'product_unavailable',
                    'product_id': product.id,
                    'product_name': product.name,
                    'message': f"Tu ne peux plus fabriquer {product.name} — il manque {', '.join(missing_articles)}",
                    'missing_articles': missing_articles
                })
        
        return alerts