# MOVETONI 定价系统设计文档（V2）

MOVETONI 是一个基于摩托车的城市出行服务平台。本系统用于根据距离、时间、天气等因素计算实时价格，并作为后端定价引擎的核心模块。

---

## 1. 定价模型

### 1.1 基础价格模型（静态）

P_base = B + α * d + β * t

参数说明：
- B：起步价 (€)
- d：距离（km）
- t：时间（min）
- α：每公里成本（电费）（可手动设置）
- β：每分钟成本（司机成本）（可手动设置）

说明：
α 和 β 不固定，由运营策略或后期数据分析动态调整。

---

### 1.2 动态定价模型（Surge）

采用线性加法模型：

S = 1 + γ1 * H + γ2 * W + γ3 * D + γ4 * E

变量说明：
- H：时间需求系数（0~1）
- W：天气系数（0~1）
- D：星期系数（0~1）
- E：特殊事件（0~2）

推荐参数：
- γ1 = 0.4（时间）
- γ2 = 0.2（天气）
- γ3 = 0.4（星期）
- γ4 = 0.5（突发事件）

---

### 1.3 最终价格

P_final = P_base * S

限制条件：

P_final = max(P_final, 3)

说明：
- 设置最低价格为 3€
- 不设置最高价格（第一版本简化）

---

## 2. 外部数据来源（API）

第一版本通过 API 自动获取：
- 距离
- 时间
- 天气
- 当前时间（系统时间）

---

### 2.1 距离 & 时间 API

推荐：
- Google Maps Distance Matrix API
- OpenRouteService API

返回数据：
- distance_km
- duration_min

---

### 2.2 天气 API

推荐：
- Open-Meteo API（免费，无需 Key）
- OpenWeatherMap API（备选）

返回数据：
- weather_condition
- rain / intensity

映射规则：

| 天气 | W |
|------|---|
| 晴天 | 0 |
| 多云 | 0.5 |
| 小雨 | 0.7 |
| 大雨 | 1 |

---

### 2.3 时间（需求 H）

根据小时划分：

| 时间段 | H |
|--------|---|
| 0-6    | 0 |
| 7      | 0.5 |
| 8-9    | 1 |
| 10-13  | 0.6 |
| 14-19  | 1 |
| 20-22  | 0.5 |
| 23     | 0.3 |

---

### 2.4 星期（D）

| 日期 | D |
|------|---|
| 周二-周五 | 0 |
| 周一 | 0.5 |
| 周末 | 1 |

---

### 2.5 特殊事件（E）

数据来源：
- 手动输入（第一版）
- 或未来接入事件 API

范围：
- 0（无）
- 1（中等事件）
- 2（重大事件）

示例：
- 演唱会
- 暴雨
- 大规模交通事故

---

## 3. 系统流程

用户输入：
- 起点
- 终点

系统执行：

1. 调用距离 API → 获取 distance_km / duration_min
2. 调用天气 API → 获取天气情况
3. 获取当前时间（系统时间）
4. 转换为 H / W / D / E
5. 计算 P_base
6. 计算 S
7. 计算最终价格 P_final
8. 返回结果

---

## 4. 核心计算逻辑（Python 伪代码）

```python
def calculate_price(origin, destination, datetime):

    distance, duration = get_distance_time(origin, destination)
    
    weather = get_weather(destination)
    
    H = get_hour_factor(datetime)
    W = get_weather_factor(weather)
    D = get_day_factor(datetime)
    E = get_event_factor()

    base_price = B + alpha * distance + beta * duration
    
    surge = 1 + gamma1*H + gamma2*W + gamma3*D + gamma4*E

    final_price = base_price * surge

    final_price = max(final_price, 3)

    return final_price

项目结构建议：
pricing_system/
│
├── main.py
├── config.py
│
├── services/
│   ├── distance_service.py
│   ├── weather_service.py
│
├── pricing/
│   ├── calculator.py
│   ├── factors.py
│
└── utils/
    └── time_utils.py

---

## 5. 运行与配置（API）

运行前可以设置环境变量（不设置时也能回退到公开服务）：
- `DISTANCE_PROVIDER`: `google` 或 `osrm`
- `GOOGLE_MAPS_API_KEY`: Google Distance Matrix Key（可选）
- 天气默认使用 Open-Meteo（免费，无需 Key）

---

## 6. 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 GOOGLE_MAPS_API_KEY（天气使用 Open-Meteo，无需 Key）

# 3. 运行
python main.py "起点地址" "终点地址"
python main.py "Madrid Sol" "Madrid Barajas" --event 1

# 4. 启动 Web 应用（可选）
streamlit run app.py
```

---

## 7. 部署到网站

可将应用部署到云端，通过 URL 在任何设备（手机、平板、电脑）访问：

| 平台 | 免费额度 | 说明 |
|------|----------|------|
| **Streamlit Cloud** | ✅ | 推荐，最简单 |
| Render | ✅ | 支持 |
| Railway | 有限 | 支持 |

**快速部署（Streamlit Cloud）：**
1. 将代码推送到 GitHub
2. 登录 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 授权
3. 新建应用，选择仓库，主文件填写 `app.py`
4. 在 Secrets 中配置 `GOOGLE_MAPS_API_KEY`
5. 部署完成后获得公开 URL

详见 [DEPLOY.md](DEPLOY.md)。