"""
定价计算核心逻辑
P_base = B + α*d + β*t
S = 1 + γ1*H + γ2*W + γ3*D + γ4*E
P_final = max(P_base * S, 3)
"""

from datetime import datetime
from typing import Optional

import config
from pricing.factors import get_event_factor, get_weather_factor
from utils.time_utils import get_day_factor, get_hour_factor


def calculate_price(
    distance_km: float,
    duration_min: float,
    weather_code: Optional[int],
    dt: Optional[datetime] = None,
    event_level: int = 0,
) -> dict:
    """
    计算最终价格

    Args:
        distance_km: 距离 (km)
        duration_min: 时长 (min)
        weather_code: Open-Meteo WMO 天气代码，用于计算 W
        dt: 时间，默认当前时间
        event_level: 特殊事件等级 0/1/2
    
    Returns:
        包含各项明细和最终价格的字典
    """
    dt = dt or datetime.now()

    H = get_hour_factor(dt)
    W = get_weather_factor(weather_code)
    D = get_day_factor(dt)
    E = get_event_factor(event_level)

    base_price = (
        config.BASE_FARE
        + config.ALPHA * distance_km
        + config.BETA * duration_min
    )

    surge = (
        1
        + config.GAMMA1 * H
        + config.GAMMA2 * W
        + config.GAMMA3 * D
        + config.GAMMA4 * E
    )

    final_price = base_price * surge
    final_price = max(final_price, config.MIN_PRICE)

    return {
        "base_price": round(base_price, 2),
        "surge_multiplier": round(surge, 3),
        "factors": {"H": H, "W": W, "D": D, "E": E},
        "final_price": round(final_price, 2),
        "distance_km": round(distance_km, 2),
        "duration_min": round(duration_min, 1),
    }
