#!/usr/bin/env python3
"""
MOVETONI - Aplicación web de cálculo de precios.
Ejecutar: streamlit run app.py
"""

import os

import streamlit as st

# Streamlit Cloud: inyectar secrets en el entorno
try:
    for k, v in st.secrets.items():
        if isinstance(v, str):
            os.environ[k] = v
except Exception:
    pass

import config
from core import get_pricing_result

st.set_page_config(
    page_title="MOVETONI - Cálculo de precios",
    page_icon="🏍️",
    layout="centered",
)

st.title("🏍️ MOVETONI")
st.markdown("### Calculadora de precios para motosharing")

st.markdown("Introduce origen y destino para obtener el precio estimado del trayecto.")

col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origen", placeholder="Ej: Madrid Sol")

with col2:
    destination = st.text_input("Destino", placeholder="Ej: Madrid Barajas")

event_level = st.selectbox(
    "Evento especial",
    options=[0, 1, 2],
    format_func=lambda x: ["Ninguno", "Medio (concierto, etc.)", "Grave (tormenta, etc.)"][x],
    index=0,
)

if st.button("Calcular precio", type="primary"):
    if not origin or not destination:
        st.error("Por favor, introduce origen y destino.")
    elif not config.GOOGLE_MAPS_API_KEY:
        st.error("GOOGLE_MAPS_API_KEY no configurada. Configure en .env")
    else:
        with st.spinner("Obteniendo ruta y tiempo..."):
            result = get_pricing_result(origin, destination, event_level)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("¡Cálculo completado!")

            st.markdown("---")
            st.markdown("#### Resultado")

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Distancia", f"{result['distance_km']} km")
            with m2:
                st.metric("Duración estimada", f"{result['duration_min']} min")
            with m3:
                st.metric("Tiempo en destino", result["weather_description"])

            st.markdown("---")
            p1, p2, p3 = st.columns(3)
            with p1:
                st.metric("Precio base", f"{result['base_price']} €")
            with p2:
                st.metric("Coef. dinámico", f"{result['surge_multiplier']}")
            with p3:
                st.metric("Precio final", f"{result['final_price']} €")

            with st.expander("Detalle de coeficientes"):
                f = result["factors"]
                st.write(f"- **H** (hora): {f['H']}")
                st.write(f"- **W** (tiempo): {f['W']}")
                st.write(f"- **D** (día): {f['D']}")
                st.write(f"- **E** (evento): {f['E']}")

st.markdown("---")
st.caption("MOVETONI - Precios calculados según distancia, tiempo y condiciones meteorológicas.")
