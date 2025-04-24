from flask import Flask, request, jsonify

from routes.pickandplace.create_gcode_routes import gcode_bp
from routes.pickandplace.deck_routes import deck_bp
from routes.pickandplace.rack_routes import rack_bp
from routes.pickandplace.preferences_routes import preferences_bp
from routes.pickandplace.routines_routes import routines_bp


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API de Pick and Place",
    "rutas disponibles": "/routines, /gcode, /preferences, /deck, /rack",
    "GCODE POST": " /gcode/protocol, /gcode/download_gcode"
    }), 200



# Registrar los blueprints
app.register_blueprint(gcode_bp, url_prefix='/gcode')
app.register_blueprint(deck_bp, url_prefix='/deck')
app.register_blueprint(rack_bp, url_prefix='/rack')
app.register_blueprint(preferences_bp, url_prefix='/preferences')
app.register_blueprint(routines_bp, url_prefix='/routines')

if __name__ == '__main__':
    app.run(debug=True, port=8000) 