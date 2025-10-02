# CCB Excel Generator

Una aplicación web simple para generar archivos Excel con datos de encuestas CCB desde la API de Hilos.

## Características

- 🚀 **Interfaz web moderna** - Frontend responsive y fácil de usar
- 📊 **Generación de Excel** - Exporta datos con encabezados personalizados
- 🔄 **Procesamiento asíncrono** - Opción de procesamiento en segundo plano
- 🌐 **CORS habilitado** - Compatible con GitHub Pages y otros hosts
- 📱 **Responsive** - Funciona en dispositivos móviles y desktop

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repositorio>
   cd ccb
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Opción 1: Ejecutar localmente

1. **Iniciar el servidor Flask:**
   ```bash
   python app.py
   ```

2. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

3. **Hacer clic en "Generar y Descargar Excel"**

### Opción 2: Desplegar en GitHub Pages

1. **Subir el archivo `index.html` a tu repositorio de GitHub Pages**

2. **Ejecutar el servidor Flask en un servicio como Heroku, Railway, o similar**

3. **Configurar la URL del servicio en la interfaz web**

## Estructura del proyecto

```
ccb/
├── app.py              # Aplicación Flask
├── ccb.py              # Lógica de extracción de datos
├── campos.json         # Mapeo de campos a encabezados
├── index.html          # Interfaz web
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```

## API Endpoints

### `GET /`
- **Descripción:** Sirve la página principal
- **Respuesta:** HTML de la interfaz web

### `GET /api/status`
- **Descripción:** Verifica el estado del servicio
- **Respuesta:** `{"status": "ok", "message": "..."}`

### `POST /api/generate-excel`
- **Descripción:** Genera y descarga el archivo Excel
- **Respuesta:** Archivo Excel (.xlsx)

### `POST /api/generate-excel-async`
- **Descripción:** Inicia procesamiento asíncrono
- **Respuesta:** `{"success": true, "job_id": "..."}`

### `GET /api/job-status/<job_id>`
- **Descripción:** Verifica el estado de un trabajo
- **Respuesta:** `{"status": "processing|completed|error", ...}`

### `GET /api/download/<job_id>`
- **Descripción:** Descarga archivo completado
- **Respuesta:** Archivo Excel (.xlsx)

## Configuración

### Token de API
El token de autorización está configurado en `app.py`. Para producción, considera usar variables de entorno:

```python
import os
AUTH_TOKEN = os.getenv('HILOS_API_TOKEN', 'tu-token-aqui')
```

### CORS
La aplicación tiene CORS habilitado para permitir llamadas desde cualquier origen. Para mayor seguridad en producción, puedes configurar dominios específicos:

```python
CORS(app, origins=['https://tu-dominio.github.io'])
```

## Personalización

### Encabezados de columnas
Edita el archivo `campos.json` para cambiar los encabezados de las columnas:

```json
{
    "campo_tecnico": "Encabezado legible",
    "phone": "Teléfono",
    "ccb_init": "Aceptación"
}
```

### Campos requeridos
Modifica la lista `required_columns` en `ccb.py` para incluir o excluir campos:

```python
self.required_columns = [
    'phone', 'ccb_init', 'ccb_adult',
    # ... otros campos
]
```

## Solución de problemas

### Error de conexión
- Verifica que el servidor Flask esté ejecutándose
- Confirma que la URL del servicio sea correcta
- Revisa que no haya problemas de firewall

### Error de token
- Verifica que el token de API sea válido
- Confirma que tenga los permisos necesarios

### Error de datos
- Revisa que el flujo ID sea correcto
- Verifica que haya datos disponibles en la API

## Desarrollo

### Ejecutar en modo debug
```bash
export FLASK_DEBUG=1
python app.py
```

### Probar solo la lógica de datos
```bash
python ccb.py --test
```

## Licencia

Este proyecto es de uso interno para CCB.

## Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
