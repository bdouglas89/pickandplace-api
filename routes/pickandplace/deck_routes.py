from flask import Blueprint, request, jsonify
import os
import json

deck_bp = Blueprint('deck', __name__)
decks = {}

@deck_bp.route('/', methods=['GET'])
def handle_decks():
   
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    deck_file = os.path.join(base_path, 'core/modules/pick_and_place/data/deck.json')
    try:
        with open(deck_file, 'r') as file:
            decks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(decks), 200

# Crear endpoint para obtener un deck por su ID
@deck_bp.route('/<int:deck_id>', methods=['GET'])
def get_deck_by_id(deck_id):
    """
    Obtener un deck por su ID
    :param deck_id: El ID del deck a obtener
    :return: El deck encontrado o un mensaje de error si no existe
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    deck_file = os.path.join(base_path, 'core/modules/pick_and_place/data/deck.json')
    try:
        with open(deck_file, 'r') as file:
            decks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    result = next((deck for deck in decks if deck["deck_id"] == deck_id), None)
    if result is None:
        return jsonify({"error": f"Deck not found: deck_id = {deck_id}"}), 404
    
    return jsonify(result), 200


@deck_bp.route('/add', methods=['POST'])
def add_deck():
    """
    Agregar un nuevo deck al archivo deck.json
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    deck_file = os.path.join(base_path, 'core/modules/pick_and_place/data/deck.json')

    try:
        # Leer el archivo JSON existente
        with open(deck_file, 'r') as file:
            decks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Obtener el nuevo deck del cuerpo de la solicitud
    new_deck = request.get_json()
    if not new_deck:
        return jsonify({"error": "No se proporcionó un deck válido en el cuerpo de la solicitud."}), 400

    # Agregar el nuevo deck a la lista
    decks.append(new_deck)

    try:
        # Guardar la lista actualizada en el archivo JSON
        with open(deck_file, 'w') as file:
            json.dump(decks, file, indent=4)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo: {str(e)}"}), 500

    return jsonify({"message": "Deck agregado exitosamente.", "deck": new_deck}), 201

@deck_bp.route('/delete/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    """
    Eliminar un deck por su ID del archivo deck.json
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    deck_file = os.path.join(base_path, 'core/modules/pick_and_place/data/deck.json')

    try:
        # Leer el archivo JSON existente
        with open(deck_file, 'r') as file:
            decks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Buscar y eliminar el deck con el ID proporcionado
    updated_decks = [deck for deck in decks if deck["deck_id"] != deck_id]
    if len(updated_decks) == len(decks):
        return jsonify({"error": f"Deck not found: deck_id = {deck_id}"}), 404

    try:
        # Guardar la lista actualizada en el archivo JSON
        with open(deck_file, 'w') as file:
            json.dump(updated_decks, file, indent=4)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo: {str(e)}"}), 500

    return jsonify({"message": f"Deck con ID {deck_id} eliminado exitosamente."}), 200