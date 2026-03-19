"""
MOVETONI 定价系统 - 配置模块
从环境变量加载 API Key 和定价参数
"""

import os
from dotenv import load_dotenv

load_dotenv()

# === API Keys ===
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
# 天气使用 Open-Meteo（免费无需 Key），OPENWEATHER_API_KEY 已废弃

# === 基础定价参数 ===
# B: 起步价 (€)
BASE_FARE = float(os.getenv("BASE_FARE", "2.5"))
# α: 每公里成本 (€/km)
ALPHA = float(os.getenv("ALPHA", "0.15"))
# β: 每分钟成本 (€/min)
BETA = float(os.getenv("BETA", "0.25"))

# === Surge 系数 ===
# γ1: 时段系数权重
GAMMA1 = float(os.getenv("GAMMA1", "0.4"))
# γ2: 天气系数权重
GAMMA2 = float(os.getenv("GAMMA2", "0.2"))
# γ3: 星期系数权重
GAMMA3 = float(os.getenv("GAMMA3", "0.4"))
# γ4: 特殊事件权重
GAMMA4 = float(os.getenv("GAMMA4", "0.5"))

# === 其他 ===
MIN_PRICE = 3.0  # 最低价格 €
