"""
时间相关工具 - 计算时段系数 H 和星期系数 D
"""

from datetime import datetime


def get_hour_factor(dt: datetime) -> float:
    """
    根据小时返回需求系数 H (0~1)
    | 时间段 | H |
    | 0-6    | 0 |
    | 7      | 0.5 |
    | 8-9    | 1 |
    | 10-13  | 0.6 |
    | 14-19  | 1 |
    | 20-22  | 0.5 |
    | 23     | 0.3 |
    """
    hour = dt.hour
    if 0 <= hour <= 6:
        return 0.0
    if hour == 7:
        return 0.5
    if 8 <= hour <= 9:
        return 1.0
    if 10 <= hour <= 13:
        return 0.6
    if 14 <= hour <= 19:
        return 1.0
    if 20 <= hour <= 22:
        return 0.5
    if hour == 23:
        return 0.3
    return 0.0


def get_day_factor(dt: datetime) -> float:
    """
    根据星期返回系数 D (0~1)
    | 周二-周五 | 0 |
    | 周一     | 0.5 |
    | 周末     | 1 |
    """
    # 0=Monday, 6=Sunday
    weekday = dt.weekday()
    if weekday == 0:  # 周一
        return 0.5
    if 1 <= weekday <= 4:  # 周二-周五
        return 0.0
    # 周六(5) 周日(6)
    return 1.0
