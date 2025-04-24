from flask import Blueprint, request, jsonify, send_file
import os
from core.modules.pick_and_place.main import create_gcode_file

gcode_bp = Blueprint('gcode', __name__)
gcode = {"gcode": "test - ok"}

#GET
@gcode_bp.route('/', methods=['GET'])
def get_gcode():
    return jsonify(gcode), 200

@gcode_bp.route('/download', methods=['GET'])
def send_dynamic_gcode():
    data = request.get_json()
    print("Data: ", data)
    file_name = data.get('filename')  # e.g. 'routine_001.gcode


    # Ruta para apuntar al directorio de archivos GCODE
    folder = "core/modules/pick_and_place/gcode_files"
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ruta base del proyecto
    file_path = os.path.join(base_path, folder, file_name)
    print("File Path: ", file_path)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not Found", "filename": file_name, "filepath":file_path}), 404

    return send_file(file_path, as_attachment=True)



@gcode_bp.route('/protocol', methods=['POST'])
def handle_gcode():
    data = request.get_json()
        
    result = create_gcode_file(data)
    if result is None:
        return jsonify({"error": "Error al crear el archivo GCODE"}), 500
    return jsonify(result), 201

