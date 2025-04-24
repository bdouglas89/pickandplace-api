"""
    lista de origen - destiono
    crear adchivo .gcode


    hacer home
    Establecer distacias apsolutas
    
    loop por cada movimiento
        ir a ubicacion origen
        bajar a distancia segura
        (Piker / Bajar a  Altura de agarre)
        (Piker / Colectar )
        (Piker / Levantar a Altura Segura)
        Ir a destino
        Bajar la muestra
        (Piker Soltar )
        Ir a Altura Segura
    fin_loop

    Finalizar el archivo.

"""

from .gcode_creator import *
from .mm_solver import *

def create_a2b(rack_data, deck_data, pick_and_drop_list):

    deck_data_coordinates = deck_data["coordinates"]

    #Contar la cantidad de movimientos (filas) del CSV
    total_movements = len(pick_and_drop_list)
    print(f"Total de movimientos: {total_movements}") 

    #Crar el archivo temporal
    create_gcode_file()

    #Establecer unidades en Milimetros
    gcode_set_mm()

    #Establecer distanciaos Apsolutas
    gcode_set_apsolute()

    #Hacer Home
    gcode_do_home_XYZ()

    #Home de Piker
    gcode_home_piker()
    gcode_macro_pickeroff()

    #Generar GCODE de los movimientos
    gcode_pick_and_drop_create(pick_and_drop_list, rack_data, deck_data_coordinates)

    #Home Final
    gcode_end(rack_data)

    #Finalizar Archivo
    rutine_info = gcode_file_rename()
    rutine_info["total_movements"] = total_movements
    rutine_info["rack_id"] = rack_data["rack_id"]
    rutine_info["rack_name"] = rack_data["name"]
    rutine_info["deck_id"] = deck_data["deck_id"]
    rutine_info["deck_name"] = deck_data["name"]
    rutine_info["deck_size_x"] = deck_data["size_x"]
    rutine_info["deck_size_y"] = deck_data["size_y"]
    
    return rutine_info

    