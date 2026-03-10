from . import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sale'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 🔐 LIAISON AVEC L'UTILISATEUR
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('sales', lazy=True, cascade="all, delete-orphan"))
    
    product = db.relationship('Product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else 'Unknown',
            'quantity': self.quantity,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id
        }