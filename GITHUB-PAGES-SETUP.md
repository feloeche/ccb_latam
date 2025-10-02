# 🚀 Configuración de GitHub Pages con Render

## 📋 **Pasos para configurar GitHub Pages**

### **1. Actualizar la URL del servicio**

**⚠️ IMPORTANTE:** Necesitas cambiar la URL en estos archivos:

#### **En `github-pages.html` (línea 280):**
```javascript
const RENDER_SERVICE_URL = 'https://ccb-latam-1.onrender.com';
```
**Cambia `tu-app.onrender.com` por tu URL real de Render**

#### **En `index.html` (línea 225):**
```html
<input type="text" id="apiUrl" placeholder="https://ccb-latam-1.onrender.com" value="https://ccb-latam-1.onrender.com">
```
**Cambia `tu-app.onrender.com` por tu URL real de Render**

### **2. Configurar GitHub Pages**

#### **Opción A: Usar la carpeta raíz**
1. Ve a tu repositorio en GitHub
2. Ve a **Settings** → **Pages**
3. En **Source**, selecciona **Deploy from a branch**
4. Selecciona **master** branch y **/ (root)**
5. Guarda los cambios

#### **Opción B: Usar la carpeta docs/ (Recomendado)**
1. Crea una carpeta `docs` en tu repositorio
2. Copia `github-pages.html` como `index.html` en la carpeta `docs/`
3. Ve a **Settings** → **Pages**
4. En **Source**, selecciona **Deploy from a branch**
5. Selecciona **master** branch y **/docs**
6. Guarda los cambios

### **3. Archivos que necesitas en GitHub Pages**

#### **Si usas la raíz:**
- `github-pages.html` → renombrar a `index.html`

#### **Si usas docs/:**
- `docs/index.html` (copia de `github-pages.html`)

### **4. Verificar configuración**

Una vez configurado, tu sitio estará disponible en:
```
https://feloeche.github.io/feloece.github.io/
```

### **5. Comandos para subir a GitHub**

```bash
# Agregar cambios
git add .

# Commit
git commit -m "Configurar GitHub Pages para Render"

# Push
git push origin master
```

## 🔧 **Configuración del servicio Render**

### **Variables de entorno en Render:**
1. Ve a tu servicio en Render
2. Ve a **Environment**
3. Agrega estas variables:
   - `HILOS_API_TOKEN`: Tu token de la API de Hilos (**REQUERIDO**)
   - `HILOS_FLOW_ID`: ID del flujo (opcional, tiene valor por defecto)
   - `FLASK_ENV`: `production` (opcional)
   - `FLASK_DEBUG`: `False` (opcional)

**⚠️ IMPORTANTE:** Sin `HILOS_API_TOKEN`, la aplicación no funcionará.

### **Configuración de dominio personalizado (opcional):**
Si tienes un dominio personalizado:
1. En Render, ve a **Settings** → **Custom Domains**
2. Agrega tu dominio
3. Actualiza la URL en los archivos HTML

## 🧪 **Pruebas**

### **1. Probar el servicio Render:**
```bash
curl https://tu-app.onrender.com/api/status
```

### **2. Probar GitHub Pages:**
1. Ve a `https://feloeche.github.io/feloece.github.io/`
2. Haz clic en "Generar y Descargar Excel"
3. Debería conectarse con Render y descargar el archivo

## ⚠️ **Consideraciones importantes**

### **Render Free Tier:**
- El servicio se "duerme" después de 15 minutos de inactividad
- La primera petición puede tomar 30+ segundos para "despertar"
- Considera usar Render Paid para producción

### **CORS:**
- El servicio ya tiene CORS configurado para GitHub Pages
- No necesitas cambios adicionales

### **Seguridad:**
- El token está en variables de entorno en Render
- No está expuesto en el código

## 🆘 **Solución de problemas**

### **Error: "El servicio no está disponible"**
- Verifica que la URL de Render sea correcta
- Espera unos minutos si es la primera petición (Render free tier)

### **Error de CORS:**
- Verifica que Flask-CORS esté instalado en Render
- Revisa que la configuración CORS esté correcta

### **Error 500 en Render:**
- Revisa los logs en Render Dashboard
- Verifica que las variables de entorno estén configuradas

## 📱 **URLs importantes**

- **GitHub Pages:** `https://feloeche.github.io/feloece.github.io/`
- **Servicio Render:** `https://tu-app.onrender.com`
- **API Status:** `https://tu-app.onrender.com/api/status`

## ✅ **Checklist de configuración**

- [ ] URL de Render actualizada en `github-pages.html`
- [ ] URL de Render actualizada en `index.html`
- [ ] GitHub Pages configurado
- [ ] Variables de entorno configuradas en Render
- [ ] Prueba de conexión exitosa
- [ ] Descarga de archivo Excel funcionando

¡Listo! Tu aplicación debería funcionar completamente desde GitHub Pages conectándose a Render. 🎉
