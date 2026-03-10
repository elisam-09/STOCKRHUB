from app import create_app
from models import db

def reset_database():
    """Recrée la base de données proprement"""
    print("🔄 Recréation de la base de données...")
    
    app = create_app()
    with app.app_context():
        # Supprime toutes les tables
        db.drop_all()
        print("🗑️ Anciennes tables supprimées")
        
        # Recrée les tables
        db.create_all()
        print("✅ Nouvelles tables créées")
        
        print("📊 Base de données prête !")

if __name__ == "__main__":
    reset_database()