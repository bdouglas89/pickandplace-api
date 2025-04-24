from .mm_solver import * 
from .gcode_creator import *
from .input_a2b import *
from .preferencestools import *

"""
    La aplicacion recibe instrucciones desde protocolo (diccionario json) en el cual se encuentran los siguientes datos:
    - deck_id: ID del deck a utilizar
    - rack_id: ID del rack a utilizar
    - steps: lista de pasos a seguir, cada paso contiene dos claves: "pick" y "place".
    - pick: indica la ubicacion de la muestra a recoger
    - place: indica la ubicacion de la muestra a depositar

    steps son 2 columnas en el formato 1A1, donde se lee de la siguiente manera:  numero de Rack , Columna de Viales, Fila de Viales.
    La primer columna "Pick" indica de donde se recoge la muestra y "Place" donde se deposita la mustra.

    Cuando se ejecuta la funcion  "create_a2b" se procesa la informacion del protocolo y se genera un archivo .gcode con el nombre routina_fechayhora.gcode

    El archivo generado ".gcode" es el que se le envia a la maquina, pero se puede hacer uso de simulador en linea para visualizar el recorrido de la maquina.
    Link de simulador: https://ncviewer.com/
    
"""




######################################################################################
# Funciones para crear el archivo .gcode desde API
######################################################################################

def create_gcode_file(protocol_data):

    deck_file = "./data/deck.json"
    rack_file = "./data/racks.json"
    
    print("\033[92m" + str(protocol_data) + "\033[0m")
    # Cargar los valores de Bandejas
    #deck_data = get_deck_coordinates(protocol_data["deck_id"], deck_file)
    deck_data = get_deck_by_id(protocol_data["deck_id"], deck_file)
    rack_data = get_rack_by_id(protocol_data["rack_id"], rack_file)
    pick_and_drop_list = json_steps_list(protocol_data)

    #Imprimir color amarillo los datos de rack, deck y pick_and_drop_list
    print("\n\n")
    print("\033[93m" + str(rack_data) + "\033[0m")
    print("\n\n")
    print("\033[93m" + str(deck_data) + "\033[0m")
    print("\n\n")
    print("\033[93m" + str(pick_and_drop_list) + "\033[0m")

    routine_info = create_a2b(rack_data, deck_data, pick_and_drop_list)
    
    print("Protocol Data: "+ "\033[92m" + str(routine_info) + "\033[0m")
    return routine_info



####################################################################
# Pruebas de las funciones
####################################################################
"""
#Carga desde JSON
protocol_path = '.\input_routines\pickandplace_01.json'
protocol_data = json_load(protocol_path)
# Imprimir en color verde el contenido del JSON cargado
print("\n\n")
print("\033[92m" + str(protocol_data) + "\033[0m")
print("\n\n")

# Cargar los valores de Bandejas
# deck_data = get_deck_coordinates(protocol_data["deck_id"])
deck_data = get_deck_by_id(protocol_data["deck_id"])

#Seleccion de Rack
rack_data = get_rack_by_id(protocol_data["rack_id"])

#Obtener el array de pasos a seguir
# Se obtiene el array dento de la llave "steps":[{"pick": "1A1", "place": "2C23"}, {"pick": "1A2", "place": "2C24"}].
pick_and_drop_list = json_steps_list(protocol_data)

print("\n\n")
print("\n\n Rack Data: ", rack_data)
print("\n\n")
print("\n\n Deck Data: ", deck_data)
print("\n\n")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
routine_info = create_a2b(rack_data, deck_data, pick_and_drop_list)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print("\n\n")
print("Protocol Data: "+ "\033[92m" + str(routine_info) + "\033[0m")
print("\n\n")

"""
