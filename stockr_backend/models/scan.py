from . import db
from datetime import datetime

class InventoryScan(db.Model):
    """Historique des scans d'inventaire réalisés par l'IA Spectra"""
    __tablename__ = 'inventory_scan'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Liaisons
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Données de l'IA
    previous_quantity = db.Column(db.Float, nullable=False)
    new_quantity = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=True) # Ex: 95.5 (Pourcentage de certitude de l'IA)
    is_manual_correction = db.Column(db.Boolean, default=False) # Si l'humain a dû corriger l'IA
    
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relations
    article = db.relationship('Article', backref=db.backref('ai_scans', lazy=True, cascade="all, delete-orphan"))
    user = db.relationship('User', backref=db.backref('scans_performed', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'article_name': self.article.name if self.article else 'Unknown',
            'previous_quantity': self.previous_quantity,
            'new_quantity': self.new_quantity,
            'confidence_score': self.confidence_score,
            'is_manual_correction': self.is_manual_correction,
            'timestamp': self.timestamp.isoformat()
        }