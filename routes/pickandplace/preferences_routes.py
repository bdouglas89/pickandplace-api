from flask import Blueprint, request, jsonify

preferences_bp = Blueprint('preferences', __name__)
preferences = {"preferences": "ok"}

@preferences_bp.route('/', methods=['GET', 'POST', 'PUT'])
def handle_preferences():
    if request.method == 'GET':
        return jsonify(preferences)
    elif request.method in ['POST', 'PUT']:
        data = request.get_json()
        preferences.update(data)
        return jsonify({"message": "Preferencias actualizadas", "preferences": preferences})
