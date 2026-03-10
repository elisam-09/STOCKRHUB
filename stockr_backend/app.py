from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routes.article_routes import article_bp
    from routes.product_routes import product_bp
    from routes.sale_routes import sale_bp
    from routes.alert_routes import alert_bp
    from routes.auth_routes import auth_bp

    app.register_blueprint(article_bp, url_prefix='/api/articles')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(sale_bp, url_prefix='/api/sales')
    app.register_blueprint(alert_bp, url_prefix='/api/alerts')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    
    @app.route('/api/health')
    def health():
        return jsonify({"status": "healthy"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)