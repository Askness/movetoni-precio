"""
距离与时长服务 - Google Maps APIs
使用 Distance Matrix API 获取距离和时长
使用 Geocoding API 获取目的地坐标（供天气 API 使用）
"""

from typing import Optional, Tuple

import requests

import config


def _geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    将地址转换为经纬度
    """
    if not config.GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY no configurada. Configure en .env")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": config.GOOGLE_MAPS_API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if data.get("status") != "OK" or not data.get("results"):
        return None

    loc = data["results"][0]["geometry"]["location"]
    return (loc["lat"], loc["lng"])


def get_distance_and_duration(
    origin: str, destination: str
) -> Optional[Tuple[float, float]]:
    """
    获取两地址之间的距离(km)和时长(min)
    
    Returns:
        (distance_km, duration_min) 或 None（调用失败时）
    """
    if not config.GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY no configurada. Configure en .env")

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": config.GOOGLE_MAPS_API_KEY,
        "mode": "driving",  # 摩托车可视为驾车模式
        "units": "metric",
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if data.get("status") != "OK":
        return None

    elements = data.get("rows", [{}])[0].get("elements", [])
    if not elements or elements[0].get("status") != "OK":
        return None

    el = elements[0]
    # distance.text 如 "5.2 km", value 是米
    # duration.text 如 "12 mins", value 是秒
    dist_m = el["distance"]["value"]
    dur_s = el["duration"]["value"]
    distance_km = dist_m / 1000
    duration_min = dur_s / 60
    return (distance_km, duration_min)


def geocode_destination(address: str) -> Optional[Tuple[float, float]]:
    """
    获取目的地坐标，供天气 API 使用
    """
    return _geocode_address(address)
