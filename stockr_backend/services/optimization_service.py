import math
from models import Article

class OptimizationService:
    
    @staticmethod
    def calculate_eoq(annual_demand, order_cost=10, holding_cost=0.2, unit_price=5):
        """
        EOQ = sqrt((2DS)/H)
        D = Annual demand
        S = Order cost per order (default 10)
        H = Holding cost per unit per year (default 20% of unit price)
        """
        if holding_cost <= 0 or annual_demand <= 0:
            return 0
        
        # Convert daily demand to annual if needed
        if annual_demand < 365:  # Assume it's daily demand
            annual_demand = annual_demand * 365
        
        eoq = math.sqrt((2 * annual_demand * order_cost) / (holding_cost * unit_price))
        return round(eoq)
    
    @staticmethod
    def recommend_reorder(article_id):
        """Generate reorder recommendation for an article"""
        article = Article.query.get(article_id)
        if not article:
            return None
        
        # Calculate EOQ
        eoq = OptimizationService.calculate_eoq(
            annual_demand=article.daily_avg_demand,  # Will be converted to annual
            order_cost=10,
            holding_cost=0.2,
            unit_price=5  # Default price, could be stored in article later
        )
        
        # Calculate how much to order
        reorder_point = article.reorder_point()
        current_stock = article.quantity
        recommended_order = 0
        
        if current_stock <= reorder_point:
            recommended_order = max(eoq, reorder_point - current_stock + article.daily_avg_demand * 7)
        
        return {
            'article_id': article.id,
            'article_name': article.name,
            'current_stock': current_stock,
            'unit': article.unit,
            'reorder_point': reorder_point,
            'daily_demand': article.daily_avg_demand,
            'lead_time_days': article.lead_time_days,
            'eoq': eoq,
            'recommended_order': int(recommended_order),
            'message': f"Commande recommandée : {int(recommended_order)} {article.unit}"
        }
    
    @staticmethod
    def get_all_recommendations():
        """Get recommendations for all low stock articles"""
        from .stock_service import StockService
        
        low_stock = StockService.get_low_stock_articles()
        recommendations = []
        
        for article in low_stock:
            rec = OptimizationService.recommend_reorder(article.id)
            if rec and rec['recommended_order'] > 0:
                recommendations.append(rec)
        
        return recommendations