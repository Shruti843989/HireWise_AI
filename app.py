import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables at the very beginning of the application startup
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from flask import Flask, send_from_directory, request, render_template
from flask_login import LoginManager
from config import Config
from database.connection import db, init_db
from models.user import User

def create_app():
    # Instantiate Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Ensure all upload/database folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize SQLite Database & SQLAlchemy
    init_db(app)
    
    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please sign in to access HireWise AI."
    login_manager.login_message_category = "warning"
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Expose upload routing to serve recorded audio and video review clips
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
    # Register Route Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.interview import interview_bp
    from routes.resume import resume_bp
    from routes.mentor import mentor_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(mentor_bp)
    
    # Context processor to inject active navigation class helpers into templates
    @app.context_processor
    def inject_helpers():
        return dict(active_nav=lambda route: 'active' if request.path.startswith(route) else '')
        
    # Global HTTP error handlers to prevent crashes and present polished templates
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_title="Page Not Found (404)", 
                               error_msg="The page you are looking for does not exist or has been relocated."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_title="Server Error (500)", 
                               error_msg="An unexpected error occurred. Please try again or check logs."), 500
                               
    return app

app = create_app()

if __name__ == '__main__':
    # Launch application locally on port 5000
    print("Launching HireWise AI on http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
