"""
天气服务 - Open-Meteo API（免费，无需 API Key）
根据经纬度获取当前天气
"""

from typing import Optional

import requests


def get_weather(lat: float, lon: float) -> Optional[dict]:
    """
    获取指定坐标的当前天气
    
    Returns:
        {
            "weather_code": int,  # WMO 天气代码
            "description": str,
            "temp": float,
            ...
        }
        失败返回 None
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "weather_code,temperature_2m,precipitation",
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if resp.status_code != 200 or "current" not in data:
        return None

    current = data["current"]
    weather_code = current.get("weather_code")
    description = _wmo_code_to_description(weather_code)

    return {
        "weather_code": weather_code,
        "description": description,
        "temp": current.get("temperature_2m"),
        "precipitation": current.get("precipitation", 0),
    }


def _wmo_code_to_description(code: Optional[int]) -> str:
    """Convierte código WMO a descripción legible en español"""
    if code is None:
        return "Desconocido"
    descriptions = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna",
        55: "Llovizna densa",
        56: "Llovizna helada ligera",
        57: "Llovizna helada densa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia helada ligera",
        67: "Lluvia helada intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        77: "Copos de nieve",
        80: "Chubascos ligeros",
        81: "Chubascos",
        82: "Chubascos intensos",
        85: "Nevadas ligeras",
        86: "Nevadas intensas",
        95: "Tormenta",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo intenso",
    }
    return descriptions.get(code, "Desconocido")
