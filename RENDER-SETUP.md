# 🚀 Configuración de Variables de Entorno en Render

## 📋 **Variables de Entorno Requeridas**

### **1. HILOS_API_TOKEN (REQUERIDO)**
- **Descripción:** Token de autorización para la API de Hilos
- **Valor:** Tu token real de la API
- **Ejemplo:** `4bc07ce70ba1bddb115d50bd54690140a3b73f96`

### **2. HILOS_FLOW_ID (OPCIONAL)**
- **Descripción:** ID del flujo específico de encuestas
- **Valor por defecto:** `0684111b-3948-7ce2-8000-b20bbb1bd564`
- **Solo cambiar si:** Tienes un flujo diferente

### **3. FLASK_ENV (OPCIONAL)**
- **Descripción:** Entorno de Flask
- **Valor recomendado:** `production`
- **Propósito:** Optimizaciones de producción

### **4. FLASK_DEBUG (OPCIONAL)**
- **Descripción:** Modo debug de Flask
- **Valor recomendado:** `False`
- **Propósito:** Desactivar debug en producción

## 🔧 **Cómo configurar en Render**

### **Paso 1: Acceder a tu servicio**
1. Ve a [render.com](https://render.com)
2. Inicia sesión en tu cuenta
3. Ve a **Dashboard**
4. Selecciona tu servicio CCB

### **Paso 2: Configurar variables**
1. En tu servicio, ve a **Environment**
2. Haz clic en **Add Environment Variable**
3. Agrega cada variable:

```
Name: HILOS_API_TOKEN
Value: tu-token-real-aqui
```

```
Name: HILOS_FLOW_ID
Value: 0684111b-3948-7ce2-8000-b20bbb1bd564
```

```
Name: FLASK_ENV
Value: production
```

```
Name: FLASK_DEBUG
Value: False
```

### **Paso 3: Guardar y redesplegar**
1. Haz clic en **Save Changes**
2. Render automáticamente redesplegará tu servicio
3. Espera a que el despliegue termine

## ✅ **Verificación**

### **1. Verificar logs**
En Render, ve a **Logs** y busca:
```
Variables de entorno configuradas correctamente
```

### **2. Probar endpoint**
```bash
curl https://ccb-latam-1.onrender.com/api/status
```

Debería responder:
```json
{
  "status": "ok",
  "message": "Servicio CCB talento latam funcionando correctamente"
}
```

### **3. Probar generación de Excel**
Desde GitHub Pages, haz clic en "Generar y Descargar Excel"

## 🚨 **Solución de Problemas**

### **Error: "HILOS_API_TOKEN es requerido"**
- ✅ Verifica que la variable esté configurada en Render
- ✅ Verifica que el nombre sea exactamente `HILOS_API_TOKEN`
- ✅ Verifica que no tenga espacios extra
- ✅ Redesplega el servicio

### **Error: "Token inválido"**
- ✅ Verifica que el token sea correcto
- ✅ Verifica que el token tenga permisos para el flujo
- ✅ Prueba el token con curl:
  ```bash
  curl -H "Authorization: Token tu-token" https://api.hilos.io/api/contact/
  ```

### **Error 500 en la aplicación**
- ✅ Revisa los logs en Render
- ✅ Verifica que todas las variables estén configuradas
- ✅ Verifica que el servicio esté desplegado correctamente

## 📱 **Comandos útiles**

### **Probar conexión a API:**
```bash
curl -H "Authorization: Token $HILOS_API_TOKEN" \
     https://api.hilos.io/api/flow-execution-contact?flow=$HILOS_FLOW_ID
```

### **Verificar variables en Render:**
En los logs de Render, busca mensajes como:
- `Variables de entorno configuradas correctamente`
- `Cargado mapeo de campos: X entradas`

## 🔐 **Seguridad**

### **✅ Buenas prácticas:**
- ✅ Nunca commites tokens en el código
- ✅ Usa variables de entorno para todos los secretos
- ✅ Rota tokens periódicamente
- ✅ Usa diferentes tokens para desarrollo y producción

### **❌ Evita:**
- ❌ Hardcodear tokens en el código
- ❌ Subir archivos .env al repositorio
- ❌ Compartir tokens en chats o emails
- ❌ Usar tokens de producción en desarrollo

## 📞 **Soporte**

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica la configuración de variables
3. Prueba la conexión a la API de Hilos
4. Contacta al administrador del sistema

¡Tu aplicación debería funcionar correctamente con estas configuraciones! 🎉
