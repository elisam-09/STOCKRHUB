from models import db, Article, Product, product_articles

class StockService:
    
    @staticmethod
    def consume_articles_for_sale(product_id, sale_quantity, user_id):
        """Consume articles for a sale (filtré par utilisateur)"""
        product = Product.query.filter_by(id=product_id, user_id=user_id).first()
        if not product or not product.composition:
            return False
        
        alerts = []
        
        for article in product.composition:
            # Vérifie que l'article appartient à l'utilisateur
            if article.user_id != user_id:
                continue
                
            query = db.session.query(product_articles).filter_by(
                product_id=product_id, article_id=article.id).first()
            qty_used = query.quantity_used if query else 1.0
            
            total_consumed = qty_used * sale_quantity
            
            if article.quantity < total_consumed:
                return False  # Not enough stock
            
            article.quantity -= total_consumed
            
            # Check if article is below threshold
            if article.is_below_threshold():
                alerts.append({
                    'article_id': article.id,
                    'name': article.name,
                    'quantity': article.quantity,
                    'unit': article.unit
                })
        
        db.session.commit()
        return alerts