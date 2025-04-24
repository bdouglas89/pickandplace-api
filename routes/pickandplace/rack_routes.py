from flask import Blueprint, request, jsonify
import os
import json

rack_bp = Blueprint('rack', __name__)
racks = {}

@rack_bp.route('/', methods=['GET'])
def handle_racks():

    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    racks_file = os.path.join(base_path, 'core/modules/pick_and_place/data/racks.json')

    try:
        with open(racks_file, 'r') as file:
            racks= json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(racks), 200
@rack_bp.route('/<int:rack_id>', methods=['GET'])
def get_rack_by_id(rack_id):
    """
    Obtener un rack por su ID
    :param rack_id: El ID del rack a obtener
    :return: El rack encontrado o un mensaje de error si no existe
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    racks_file = os.path.join(base_path, 'core/modules/pick_and_place/data/racks.json')

    try:
        # Leer el archivo JSON existente
        with open(racks_file, 'r') as file:
            racks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Buscar el rack con el ID proporcionado
    rack = next((rack for rack in racks if rack["rack_id"] == rack_id), None)
    if rack is None:
        return jsonify({"error": f"Rack not found: rack_id = {rack_id}"}), 404

    return jsonify(rack), 200


@rack_bp.route('/add', methods=['POST'])
def add_rack():
    """
    Agregar un nuevo rack al archivo racks.json
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    racks_file = os.path.join(base_path, 'core/modules/pick_and_place/data/racks.json')

    try:
        # Leer el archivo JSON existente
        with open(racks_file, 'r') as file:
            racks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Obtener el nuevo rack del cuerpo de la solicitud
    new_rack = request.get_json()
    if not new_rack:
        return jsonify({"error": "No se proporcionó un rack válido en el cuerpo de la solicitud."}), 400

    # Agregar el nuevo rack a la lista
    racks.append(new_rack)

    try:
        # Guardar la lista actualizada en el archivo JSON
        with open(racks_file, 'w') as file:
            json.dump(racks, file, indent=4)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo: {str(e)}"}), 500

    return jsonify({"message": "Rack agregado exitosamente.", "rack": new_rack}), 201



@rack_bp.route('/delete/<int:rack_id>', methods=['DELETE'])
def delete_rack(rack_id):
    """
    Eliminar un rack por su ID del archivo racks.json
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    racks_file = os.path.join(base_path, 'core/modules/pick_and_place/data/racks.json')

    try:
        # Leer el archivo JSON existente
        with open(racks_file, 'r') as file:
            racks = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo no existe."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "El archivo no es un JSON válido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Buscar y eliminar el rack con el ID proporcionado
    updated_racks = [rack for rack in racks if rack["rack_id"] != rack_id]
    if len(updated_racks) == len(racks):
        return jsonify({"error": f"Rack not found: rack_id = {rack_id}"}), 404

    try:
        # Guardar la lista actualizada en el archivo JSON
        with open(racks_file, 'w') as file:
            json.dump(updated_racks, file, indent=4)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo: {str(e)}"}), 500

    return jsonify({"message": f"Rack con ID {rack_id} eliminado exitosamente."}), 200