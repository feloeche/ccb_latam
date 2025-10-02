# Instrucciones de Instalación - CCB Excel Generator

## Instalación Rápida

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python app.py
```

### 3. Abrir en el navegador
```
http://localhost:8080
```

## Despliegue en Servicios Web

### Opción 1: Railway (Recomendado)

1. **Crear cuenta en Railway:**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu cuenta de GitHub

2. **Desplegar desde GitHub:**
   - Haz fork de este repositorio
   - En Railway, selecciona "Deploy from GitHub repo"
   - Selecciona tu repositorio fork
   - Railway detectará automáticamente que es una app Python

3. **Configurar variables de entorno:**
   - En Railway, ve a Variables
   - Agrega `HILOS_API_TOKEN` con tu token de API

4. **Obtener URL del servicio:**
   - Railway te dará una URL como `https://tu-app.railway.app`
   - Usa esta URL en la interfaz web

### Opción 2: Render

1. **Crear cuenta en Render:**
   - Ve a [render.com](https://render.com)
   - Conecta tu cuenta de GitHub

2. **Crear nuevo Web Service:**
   - Selecciona tu repositorio
   - Usa estos ajustes:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
     - **Environment:** Python 3

3. **Configurar variables:**
   - En Environment Variables, agrega:
     - `HILOS_API_TOKEN`: tu token de API

### Opción 3: Heroku

1. **Instalar Heroku CLI:**
   ```bash
   # En macOS
   brew install heroku/brew/heroku
   
   # En Windows
   # Descargar desde heroku.com
   ```

2. **Login y crear app:**
   ```bash
   heroku login
   heroku create tu-app-ccb
   ```

3. **Configurar variables:**
   ```bash
   heroku config:set HILOS_API_TOKEN=tu-token-aqui
   ```

4. **Desplegar:**
   ```bash
   git push heroku main
   ```

## Configuración para GitHub Pages

### 1. Subir archivos estáticos
- Sube `gh-pages.html` como `index.html` a tu repositorio de GitHub Pages
- O usa GitHub Pages para servir desde la carpeta `docs/`

### 2. Configurar URL del servicio
- En la interfaz web, actualiza la URL del servicio con la URL de tu servicio desplegado

## Variables de Entorno

### Desarrollo Local
```bash
export HILOS_API_TOKEN="tu-token-aqui"
```

### Producción
Configura estas variables en tu servicio de hosting:
- `HILOS_API_TOKEN`: Token de autorización para la API de Hilos
- `FLASK_ENV`: `production` (opcional)

## Solución de Problemas

### Error: "Unable to import flask"
```bash
pip install flask flask-cors
```

### Error: "No module named 'ccb'"
Asegúrate de que `ccb.py` esté en el mismo directorio que `app.py`

### Error de CORS
Si tienes problemas de CORS, verifica que Flask-CORS esté instalado:
```bash
pip install flask-cors
```

### Error de permisos en Windows
```bash
# Ejecutar como administrador o usar
python -m pip install --user -r requirements.txt
```

### Puerto ocupado
Si el puerto 5000 está ocupado, puedes cambiarlo:
```python
# En app.py, línea final
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Verificación

### 1. Verificar servicio
```bash
curl http://localhost:8080/api/status
```

### 2. Probar generación de Excel
- Abre `http://localhost:8080`
- Haz clic en "Generar y Descargar Excel"
- Debería descargarse el archivo `ccb_data.xlsx`

### 3. Verificar archivo Excel
- Abre el archivo descargado
- Verifica que tenga las columnas con encabezados correctos
- Confirma que contenga datos

## Estructura Final

Después de la instalación, tu proyecto debería verse así:
```
ccb/
├── app.py              # ✅ Aplicación Flask
├── ccb.py              # ✅ Lógica de extracción
├── campos.json         # ✅ Mapeo de encabezados
├── index.html          # ✅ Interfaz web
├── gh-pages.html       # ✅ Versión para GitHub Pages
├── requirements.txt    # ✅ Dependencias
├── README.md          # ✅ Documentación
└── INSTALACION.md     # ✅ Este archivo
```

## Soporte

Si tienes problemas:
1. Revisa los logs del servicio
2. Verifica que el token de API sea válido
3. Confirma que la API de Hilos esté funcionando
4. Revisa que todas las dependencias estén instaladas
