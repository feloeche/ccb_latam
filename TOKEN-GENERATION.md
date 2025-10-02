# 🔐 Generación de Tokens de Acceso

## 📋 **Sistema de Autenticación**

La aplicación ahora usa un sistema de autenticación de dos niveles:

### **1. Token de Hilos (Backend)**
- **Uso:** Para acceder a la API de Hilos
- **Alcance:** Solo el servidor backend
- **Variable:** `HILOS_API_TOKEN`
- **Seguridad:** Nunca se expone al frontend

### **2. Token de Acceso (Frontend)**
- **Uso:** Para acceder a los endpoints de la aplicación
- **Alcance:** Usuarios autorizados
- **Variable:** `FRONTEND_ACCESS_TOKEN`
- **Seguridad:** Se comparte con usuarios autorizados

## 🎯 **Generar Token de Acceso**

### **Opción 1: Token Simple**
```bash
# Generar token simple con fecha
echo "ccb-access-$(date +%Y%m%d)-$(openssl rand -hex 4)"
```

### **Opción 2: Token UUID**
```bash
# Generar UUID (requiere uuidgen o python)
uuidgen | tr '[:upper:]' '[:lower:]'
```

### **Opción 3: Token Aleatorio**
```bash
# Generar token aleatorio de 32 caracteres
openssl rand -hex 16
```

### **Opción 4: Token Descriptivo**
```bash
# Token con formato descriptivo
echo "ccb-talento-latam-$(date +%Y)-$(openssl rand -hex 6)"
```

## 📝 **Ejemplos de Tokens Válidos**

### **Formato 1: Con fecha**
```
ccb-access-20250102-a1b2c3d4
ccb-access-20250102-xyz789abc
```

### **Formato 2: UUID**
```
550e8400-e29b-41d4-a716-446655440000
6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

### **Formato 3: Hexadecimal**
```
a1b2c3d4e5f6789012345678901234ab
fedcba0987654321fedcba0987654321
```

### **Formato 4: Descriptivo**
```
ccb-talento-latam-2025-abc123def456
ccb-talento-latam-2025-xyz789uvw012
```

## ⚙️ **Configuración en Render**

### **1. Generar tu token:**
```bash
# Ejemplo usando openssl
TOKEN=$(openssl rand -hex 16)
echo "Tu token de acceso: $TOKEN"
```

### **2. Configurar en Render:**
1. Ve a tu servicio en Render
2. Ve a **Environment**
3. Agrega:
   ```
   Name: FRONTEND_ACCESS_TOKEN
   Value: tu-token-generado-aqui
   ```

### **3. Compartir con usuarios:**
- Envía el token solo a usuarios autorizados
- Usa canales seguros (no email o chat)
- Considera rotar el token periódicamente

## 🔄 **Rotación de Tokens**

### **Cuándo rotar:**
- ✅ Mensualmente (recomendado)
- ✅ Cuando sospeches compromiso
- ✅ Cuando un usuario deje de necesitar acceso
- ✅ Después de cambios de seguridad

### **Cómo rotar:**
1. **Generar nuevo token**
2. **Actualizar en Render** (Environment)
3. **Notificar a usuarios** el nuevo token
4. **Verificar funcionamiento**

## 🛡️ **Mejores Prácticas**

### **✅ Hacer:**
- ✅ Usar tokens únicos y aleatorios
- ✅ Rotar tokens regularmente
- ✅ Compartir tokens por canales seguros
- ✅ Documentar quién tiene acceso
- ✅ Usar tokens diferentes para dev/prod

### **❌ Evitar:**
- ❌ Tokens predecibles (123456, password, etc.)
- ❌ Compartir tokens por email/chat
- ❌ Usar el mismo token para todo
- ❌ Tokens que no expiren
- ❌ Hardcodear tokens en el código

## 📊 **Gestión de Acceso**

### **Usuarios autorizados:**
- **Administradores:** Acceso completo
- **Analistas:** Solo descarga de datos
- **Desarrolladores:** Solo para testing

### **Control de acceso:**
- Mantén lista de usuarios autorizados
- Revoca acceso cuando sea necesario
- Monitorea uso de tokens
- Registra accesos (logs)

## 🚨 **Solución de Problemas**

### **Error: "Token de acceso requerido"**
- ✅ Verificar que el token esté configurado en Render
- ✅ Verificar que el usuario ingrese el token correcto
- ✅ Verificar formato Bearer en el header

### **Error 401 Unauthorized**
- ✅ Verificar que el token coincida exactamente
- ✅ Verificar que no haya espacios extra
- ✅ Verificar que el token no haya expirado

### **Error de conexión**
- ✅ Verificar que Render esté funcionando
- ✅ Verificar que las variables estén configuradas
- ✅ Revisar logs de Render

## 📞 **Soporte**

Para problemas con tokens:
1. Verifica la configuración en Render
2. Prueba con un token nuevo
3. Revisa los logs del servidor
4. Contacta al administrador

¡Mantén tus tokens seguros! 🔐
