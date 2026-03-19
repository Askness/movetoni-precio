"""
定价系数 - 天气 W、特殊事件 E
支持 Open-Meteo WMO 天气代码
W: 晴天=0, 多云=0.5, 小雨=0.7, 大雨=1
"""

from typing import Optional

# 天气代码到 W 系数的映射（Open-Meteo WMO 代码）
# 参考: https://open-meteo.com/en/docs
WEATHER_CODE_TO_W = {
    # 晴天 W=0
    0: 0.0,
    # 多云 W=0.5
    1: 0.5,
    2: 0.5,
    3: 0.5,
    45: 0.5,
    48: 0.5,
    # 毛毛雨/小雨 W=0.7
    51: 0.7,
    53: 0.7,
    55: 0.7,
    56: 0.7,
    57: 0.7,
    61: 0.7,
    71: 0.7,
    77: 0.7,
    80: 0.7,
    85: 0.7,
    # 中雨/大雨 W=1
    63: 1.0,
    65: 1.0,
    66: 1.0,
    67: 1.0,
    73: 1.0,
    75: 1.0,
    81: 1.0,
    82: 1.0,
    86: 1.0,
    95: 1.0,
    96: 1.0,
    99: 1.0,
}


def get_weather_factor(weather_code: Optional[int]) -> float:
    """
    根据天气代码（Open-Meteo WMO）返回天气系数 W
    未知天气默认 0.5（多云）
    """
    if weather_code is None:
        return 0.5
    return WEATHER_CODE_TO_W.get(weather_code, 0.5)


def get_event_factor(event_level: int = 0) -> float:
    """
    特殊事件系数 E
    0: 无, 1: 中等, 2: 重大
    第一版由调用方手动传入
    """
    return float(max(0, min(2, event_level)))
