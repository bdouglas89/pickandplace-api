from flask import Blueprint, request, jsonify
import json
import os

routines_bp = Blueprint('routines', __name__)
routines = {"routines": "test - ok"}

@routines_bp.route('/', methods=['GET', 'POST'])
def list_gcode_files():
    """
    Listar todos los archivos .gcode dentro de la carpeta gcode_files
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    gcode_folder = os.path.join(base_path, 'core/modules/pick_and_place/gcode_files')

    try:
        # Verificar si la carpeta existe
        if not os.path.exists(gcode_folder):
            return jsonify({"error": "La carpeta gcode_files no existe."}), 404

        # Listar todos los archivos .gcode
        gcode_files = [file for file in os.listdir(gcode_folder) if file.endswith('.gcode')]

        return jsonify({"gcode_files": gcode_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Eliminar un archivo .gcode
@routines_bp.route('/delete', methods=['DELETE'])
def delete_gcode_file():
    """
    Eliminar un archivo .gcode dentro de la carpeta gcode_files
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    gcode_folder = os.path.join(base_path, 'core/modules/pick_and_place/gcode_files')
    
    data = request.get_json()
    file_name = data.get('file_name') if data else None

    #print request.args
    print(request.get_json())

    # Validar que se haya proporcionado el nombre del archivo
    if not file_name:
        return jsonify({"error": "El parámetro 'file_name' es obligatorio."}), 400

    file_path = os.path.join(gcode_folder, file_name)

    try:
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            return jsonify({"error": f"El archivo '{file_name}' no existe."}), 404

        # Eliminar el archivo
        os.remove(file_path)

        return jsonify({"message": f"Archivo '{file_name}' eliminado exitosamente."}), 200
    except PermissionError:
        return jsonify({"error": f"No se pudo eliminar el archivo '{file_name}' debido a permisos insuficientes."}), 403
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el archivo: {str(e)}"}), 500