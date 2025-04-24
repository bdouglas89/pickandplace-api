import json
import os
###########################################################################################
#  Funcionen para cargar JSON, desde una ruta especifica
###########################################################################################
def json_load(filename):
    """
    Carga un archivo JSON y devuelve su contenido como una lista de diccionarios.
    :param json_path: Ruta al archivo JSON.
    :return: Lista de diccionarios con el contenido del archivo JSON.
    """
    try:
        """
        # Obtener la ruta absoluta basada en la ubicación del archivo actual
        json_path = filename
        """
        base_path = os.path.dirname(__file__)  # Ruta del directorio actual
        json_path = os.path.join(base_path, filename)  # Construir la ruta completa
        # Comprobar si el archivo existe
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"El archivo no existe.--------->  {json_path}")
        print(f"Intentando cargar el archivo: {json_path}")

        with open(json_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: El archivo {json_path} no se encontró.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {json_path} no es un JSON válido.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []




#########################################################################################
#  Funciones relacionadas a Deck
#########################################################################################



# Optener del array de decks el deck que se desea usar
def get_deck_by_id(deck_id, deck_json_path):
    """
    Obtiene el deck por su ID
    :param deck_id: El ID del deck a obtener
    :return: El deck encontrado o un mensaje de error si no existe
    """
    data = json_load(deck_json_path)
    if not data:
        return {"error": "No data found in the JSON file."}
    else:
        # Validar si el deck existe
        if deck_id not in [item["deck_id"] for item in data]:
            return {"error": f"Deck not found: deck_id = {deck_id}"}
        deck = next((item for item in data if item["deck_id"] == deck_id), None)
        print("Datos del Deck Seleccionado: ", deck)
        return deck

# Obtener las coordenadas de las bandejas de un deck
def get_deck_coordinates(deck_id, deck_json_path):
    """
    Obtiene las coordenadas de las bandejas de un deck
    :param deck_id: El ID del deck a obtener
    :return: Las coordenadas de las bandejas o un mensaje de error si no existe
    """
    deck = get_deck_by_id(deck_id, deck_json_path)
    if "error" in deck:
        return deck
    return deck["coordinates"]

#########################################################################################
#  Funciones relacionadas a Rack
#########################################################################################

# Funcion para obtener el rack por su ID
def get_rack_by_id(rack_id, rack_json_path):
    data = json_load(rack_json_path)

    if not data:
        return {"error": "No data found in the JSON file."}
    # Validar si el rack existe
    if rack_id not in [item["rack_id"] for item in data]:
        return {"error": f"Rack not found: rack_id = {rack_id}"}
    rack = next((item for item in data if item["rack_id"] == rack_id), None)
    print("Datos del Racks Seleccionado: ", rack)
    return rack


################################################################################
# Funcionpara crear pick_and_place_list desde archivo JSON
#################################################################################

def json_steps_list(protocol):
    """
    Obtiene el array dento de la llave "steps":[{"pick": "1A1", "place": "2C23"}, {"pick": "1A2", "place": "2C24"}].
    Para cada elemento del array se obtiene el valor de "pick" y "place".
    Se crea una lista de tuplas con los valores obtenidos y se devuelve la lista.

    Args:
    - nombre_archivo (str): La ruta al archivo JSON que se va a leer.

    """
    pick_and_drop_list = []

    print("\nMovimientos a realizar:")
    print("=====================================")

    for i, step in enumerate(protocol["steps"], start=1):
        pick_and_drop_list.append((step["pick"], step["place"]))
        print(f"#{i}:   {step['pick']}  --> {step['place']}")
    
    print("=====================================")
    
    return pick_and_drop_list
        


