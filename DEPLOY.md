# MOVETONI - Guía de despliegue web

Este documento explica cómo desplegar la calculadora de precios MOVETONI en un sitio web accesible desde cualquier dispositivo.

---

## Opción 1: Streamlit Community Cloud (Recomendado - Gratis)

### Requisitos
- Cuenta en [GitHub](https://github.com)
- Cuenta en [Streamlit Community Cloud](https://share.streamlit.io)

### Pasos

1. **Subir el código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "MOVETONI pricing app"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/movetoni-precio.git
   git push -u origin main
   ```

2. **Desplegar en Streamlit Cloud**
   - Ir a [share.streamlit.io](https://share.streamlit.io)
   - "Sign in with GitHub"
   - "New app"
   - Repositorio: `TU_USUARIO/movetoni-precio`
   - Branch: `main`
   - Main file path: `app.py`
   - En **Advanced settings** → **Secrets**, añadir:
     ```
     GOOGLE_MAPS_API_KEY = "tu_api_key_aquí"
     ```

3. **Listo** – Obtendrás una URL como:
   ```
   https://movetoni-precio-xxx.streamlit.app
   ```

---

## Opción 2: Render (Gratis)

1. Crear cuenta en [render.com](https://render.com)
2. "New" → "Web Service"
3. Conectar repositorio GitHub
4. Configuración:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. En Variables de entorno, añadir `GOOGLE_MAPS_API_KEY`

---

## Opción 3: Railway (Gratis con límites)

1. [railway.app](https://railway.app) → "Start a New Project" → "Deploy from GitHub"
2. Seleccionar repositorio
3. Añadir variable `GOOGLE_MAPS_API_KEY`
4. Railway detectará automáticamente la app

---

## Opción 4: Ejecutar en local (pruebas)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre http://localhost:8501 en el navegador (o en tu red local desde el móvil usando tu IP).

---

## Notas sobre API Key

- **Nunca** subas `.env` al repositorio (está en `.gitignore`)
- En producción usa los "Secrets" o "Variables de entorno" de la plataforma
- Restringe la API Key en Google Cloud Console si es posible (por dominio o IP)
