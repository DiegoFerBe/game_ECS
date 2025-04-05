# utils/json_loader.py
import json
from typing import Any

def load_json(file_path: str,key: str = None) -> Any:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if key is not None:
            if key in data:
                return data[key]
            else:
                raise KeyError(f"La clave '{key}' no se encontró en el JSON de {file_path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar JSON en {file_path}: {e}")