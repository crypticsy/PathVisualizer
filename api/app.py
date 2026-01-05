from flask import render_template, Flask
from api.api_routes import api_bp

# initialize the Flask app
app = Flask(__name__)

# Register API blueprint
app.register_blueprint(api_bp)

@app.route('/', methods=['GET'])
def home():
    # Simply render the template without running algorithms
    # All pathfinding is now handled via API endpoints
    return render_template('home.html')