"""
MOVETONI - Lógica central de cálculo de precios.
Obtiene ruta, tiempo y calcula el precio.
"""

from typing import Any, Dict, Optional

import config
from pricing.calculator import calculate_price
from services.distance_service import geocode_destination, get_distance_and_duration
from services.weather_service import get_weather


def get_pricing_result(
    origin: str, destination: str, event_level: int = 0
) -> Dict[str, Any]:
    """
    Obtiene ruta, tiempo meteorológico y calcula el precio.

    Returns:
        Si éxito: dict con base_price, surge_multiplier, factors, final_price,
                  distance_km, duration_min, weather_description
        Si error: dict con "error": str
    """
    dist_result = get_distance_and_duration(origin, destination)
    if not dist_result:
        return {"error": "No se pudo obtener distancia y duración. Compruebe la dirección."}

    distance_km, duration_min = dist_result

    coords = geocode_destination(destination)
    weather_code = None
    weather_description = "Desconocido"

    if coords:
        weather_data = get_weather(coords[0], coords[1])
        if weather_data:
            weather_code = weather_data.get("weather_code")
            weather_description = weather_data.get("description", "Desconocido")

    result = calculate_price(
        distance_km=distance_km,
        duration_min=duration_min,
        weather_code=weather_code,
        event_level=event_level,
    )
    result["weather_description"] = weather_description
    return result
