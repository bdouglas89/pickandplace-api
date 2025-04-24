# API Generadora de G-code para Robot Pick and Place

Esta API permite generar código G para un robot pick and place que maneja cajas de viales.

## Estructura del Proyecto

```
.
├── app.py
├── core/
│   └── modules/
│       └── pick_and_place/
│           └── gcode_generator.py
└── requirements.txt
```

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar el servidor:
```bash
python app.py
```

2. Enviar una petición POST a `http://localhost:5000/generate-gcode` con el siguiente formato:
```json
{
    "positions": [
        {"x": 100, "y": 100, "z": 0},
        {"x": 200, "y": 200, "z": 0}
    ]
}
```

## Parámetros

- `positions`: Lista de posiciones donde se encuentran las cajas de viales
  - `x`: Coordenada X en milímetros
  - `y`: Coordenada Y en milímetros
  - `z`: Coordenada Z en milímetros

## Respuesta

La API devuelve un objeto JSON con el código G generado:
```json
{
    "status": "success",
    "gcode": "G21\nG90\n..."
}
``` 