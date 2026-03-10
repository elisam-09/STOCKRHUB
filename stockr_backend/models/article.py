from . import db

class Article(db.Model):
    __tablename__ = 'article'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(20), nullable=False, default='pcs')
    alert_threshold = db.Column(db.Float, nullable=True)
    daily_avg_demand = db.Column(db.Float, nullable=False, default=1.0)
    lead_time_days = db.Column(db.Integer, nullable=False, default=7)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('articles', lazy=True, cascade="all, delete-orphan"))

    def reorder_point(self):
        return self.daily_avg_demand * self.lead_time_days
    
    def is_below_threshold(self):
        if self.alert_threshold:
            return self.quantity <= self.alert_threshold
        return self.quantity <= self.reorder_point()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'alert_threshold': self.alert_threshold,
            'daily_avg_demand': self.daily_avg_demand,
            'lead_time_days': self.lead_time_days,
            'reorder_point': self.reorder_point(),
            'is_low': self.is_below_threshold()
        }