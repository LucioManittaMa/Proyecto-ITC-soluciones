# Documentación API AWS-Sender - Envío de Emails

## Descripción General

La API AWS-Sender es un servicio de envío de emails que utiliza Amazon Simple Email Service (SES) para el envío de correos electrónicos. La API soporta dos tipos principales de envío:

1. **Envío de emails simples** con contenido HTML codificado en Base64
2. **Envío de emails con templates** y archivos adjuntos

## Información Base

- **URL Base**: `http://localhost:${EMAIL_PORT}` (configurable)
- **Protocolo**: HTTP/HTTPS
- **Formato de datos**: JSON
- **Autenticación**: No requerida (configuración interna de AWS)

---

## Endpoints Disponibles

### 1. Envío de Email Simple

**Endpoint**: `POST /sendEmail`

**Descripción**: Envía un email con contenido HTML codificado en Base64.

#### Request Body

```json
{
  "toEmail": "string",
  "fromEmail": "string", 
  "htmlEncoded": "string",
  "subject": "string"
}
```

#### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `toEmail` | string | Sí | Dirección de correo del destinatario |
| `fromEmail` | string | Sí | Dirección de correo del remitente |
| `htmlEncoded` | string | Sí | Contenido HTML codificado en Base64 |
| `subject` | string | Sí | Asunto del email |

#### Response

**Código de éxito**: 200

```json
{
  "status": 200,
  "mensaje": "Email enviado exitosamente!"
}
```

**Código de error**: 500

```json
{
  "status": 500,
  "mensaje": "Error al enviar el email. Código de estado: [código]"
}
```

#### Ejemplo de Request

```json
{
  "toEmail": "usuario@ejemplo.com",
  "fromEmail": "noreply@miempresa.com",
  "htmlEncoded": "PGgxPkFzYW50byBkZWwgZW1haWw8L2gxPjxwPkVzdGUgZXMgdW4gZW1haWwgcHJ1ZWJhPC9wPg==",
  "subject": "Prueba de Email"
}
```

---

### 2. Envío de Email con Template y Adjunto

**Endpoint**: `POST /sendTemplateMessageWithAttachment`

**Descripción**: Envía un email utilizando templates predefinidos con posibilidad de adjuntar archivos.

#### Request Body

```json
{
  "fromEmail": "string",
  "toEmail": "string",
  "subject": "string",
  "body": "string", i
  "cc": ["string"],
  "bcc": ["string"],
  "sentDate": "2024-01-01T00:00:00.000Z",
  "link": "string",
  "attachment": "string",
  "linkAceptacion": "string",
  "linkRechazo": "string",
  "nombreUsuario": "string",
  "nombreAdmin": "string",
  "emailAdmin": "string",
  "codInstalacion": "string",
  "domicilio": "string",
  "nombrePrescriptor": "string",
  "apellidoPrescriptor": "string",
  "indicaciones": "string",
  "adjunto": "byte[]",
  "cuitFinanciador": "string"
}
```

#### Parámetros Requeridos

| Campo | Tipo | Validación | Descripción |
|-------|------|------------|-------------|
| `fromEmail` | string | Email válido | Dirección de correo del remitente |
| `toEmail` | string | Email válido | Dirección de correo del destinatario |
| `subject` | string | No vacío | Asunto del email |
| `body` | string | No vacío | Cuerpo del mensaje |
| `aplicacion` | string | No vacío | Aplicación origen (NUVALID, TURNEA, NUVALID-FARMACIA, etc.) |

#### Parámetros Opcionales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `replyTo` | string | Dirección de respuesta |
| `to` | string[] | Lista de destinatarios adicionales |
| `cc` | string[] | Lista de destinatarios en copia |
| `bcc` | string[] | Lista de destinatarios en copia oculta |
| `sentDate` | Date | Fecha de envío |
| `link` | string | Enlace para incluir en el template |
| `attachment` | string | Archivo adjunto (ruta) |
| `linkAceptacion` | string | Enlace de aceptación |
| `linkRechazo` | string | Enlace de rechazo |
| `nombreUsuario` | string | Nombre del usuario |
| `nombreAdmin` | string | Nombre del administrador |
| `emailAdmin` | string | Email del administrador |
| `codInstalacion` | string | Código de instalación |
| `domicilio` | string | Domicilio |
| `nombrePrescriptor` | string | Nombre del prescriptor |
| `apellidoPrescriptor` | string | Apellido del prescriptor |
| `indicaciones` | string | Indicaciones médicas |
| `adjunto` | byte[] | Archivo adjunto en bytes |
| `cuitFinanciador` | string | CUIT del financiador |

#### Response

**Código de éxito**: 200

```json
"Email con template y attachment enviado correctamente"
```

**Código de error**: 400

```json
{
  "mensaje": "Debe enviar un asunto para el mail"
}
```

---

## Templates Disponibles

La API soporta los siguientes templates según el asunto del email:

### Templates de NUVALID

| Asunto | Template | Descripción |
|--------|----------|-------------|
| `Confirmar Cuenta en Nuvalid` | `nuvalid/confirmar-cuenta` | Confirmación de cuenta de usuario |
| `Cambiar cuenta de correo - NUVALID` | `nuvalid/cambiar-mail` | Cambio de dirección de correo |
| `Registro de un nuevo usuario - NUVALID` | `nuvalid/nuevo-usuario` | Notificación de nuevo usuario |
| `Cambio de contraseña - NUVALID` | `nuvalid/restablecer-contrasenna` | Cambio de contraseña |
| `Petición Usuario Aceptada - NUVALID` | `nuvalid/usuario-aceptado` | Usuario aceptado |
| `Sugerencia para Nuvalid` | `nuvalid/sugerencias` | Formulario de sugerencias |
| `Instalar Nuvalid` | `nuvalid/instalar-nuvalid` | Instalación de aplicación |

### Templates de TURNEA

| Asunto | Template | Descripción |
|--------|----------|-------------|
| `Confirmar Cuenta en Turnea` | `turnea/confirmar-cuenta` | Confirmación de cuenta |
| `Cambio de contraseña - TURNEA` | `turnea/reestablecer-contrasenia` | Cambio de contraseña |

### Templates de NUVALID-FARMACIA

| Asunto | Template | Descripción |
|--------|----------|-------------|
| `Confirmar Cuenta en Nuvalid` | `nuvalid-farmacia/confirmar-cuenta1` | Confirmación de cuenta farmacia |
| `Cambiar cuenta de correo - NUVALID` | `nuvalid-farmacia/cambiar-mail1` | Cambio de correo farmacia |
| `Instalar Nuvalid Farmacia` | `nuvalid-farmacia/instalar-nuvalid-farmacia` | Instalación farmacia |

### Templates de Prescripciones

| Asunto | Template | Descripción |
|--------|----------|-------------|
| `Nuevas indicaciones` | `MPOS/envioPrescripcion` | Envío de prescripción médica |
| `Publicidad Nuevas indicaciones` | `MPOS/PublicidadEnvioPrescripcion` | Prescripción con publicidad |

### Templates de DOCTRA

| Asunto | Template | Descripción |
|--------|----------|-------------|
| `Cambio de estado de orden - Doctra` | `doctra/mail-doctra-cambio-estado` | Cambio de estado de orden |

---

## Ejemplos de Uso

### Ejemplo 1: Email Simple

```bash
curl -X POST http://localhost:8080/sendEmail \
  -H "Content-Type: application/json" \
  -d '{
    "toEmail": "usuario@ejemplo.com",
    "fromEmail": "noreply@miempresa.com",
    "subject": "Bienvenido",
    "htmlEncoded": "PGgxPkJpZW52ZW5pZG88L2gxPjxwPkdyYWNpYXMgcG9yIHJlZ2lzdHJhcnRlPC9wPg=="
  }'
```

### Ejemplo 2: Email con Template de Confirmación

```bash
curl -X POST http://localhost:8080/sendTemplateMessageWithAttachment \
  -H "Content-Type: application/json" \
  -d '{
    "fromEmail": "noreply@miempresa.com",
    "toEmail": "usuario@ejemplo.com",
    "subject": "Confirmar Cuenta en Nuvalid",
    "body": "Por favor confirma tu cuenta",
    "aplicacion": "NUVALID",
    "nombreUsuario": "Juan Pérez",
    "link": "https://miempresa.com/confirmar?token=abc123"
  }'
```

### Ejemplo 3: Email de Prescripción con Adjunto

```bash
curl -X POST http://localhost:8080/sendTemplateMessageWithAttachment \
  -H "Content-Type: application/json" \
  -d '{
    "fromEmail": "prescripcion-nuvalid@notificaciones.ar",
    "toEmail": "farmacia@ejemplo.com",
    "subject": "Nuevas indicaciones",
    "body": "15 Jan 2024",
    "aplicacion": "NUVALID-FARMACIA",
    "nombreUsuario": "María García",
    "nombrePrescriptor": "Dr. Juan",
    "apellidoPrescriptor": "López",
    "indicaciones": "Tomar cada 8 horas",
    "adjunto": "[bytes del archivo PDF]",
    "cuitFinanciador": "30546741253"
  }'
```

---

## Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 200 | Éxito | Email enviado correctamente |
| 400 | Bad Request | Verificar parámetros requeridos |
| 500 | Error interno | Error en el servicio AWS SES |

---

## Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `EMAIL_PORT` | Puerto del servidor | `8080` |
| `API_AWSKEY` | Clave de API de AWS | `AKIA...` |

### Configuración SMTP

- **Protocolo**: SMTP
- **Puerto**: 587
- **TLS**: Habilitado
- **Autenticación**: Requerida

---

## Notas Importantes

1. **Validación de Emails**: Todos los campos de email deben tener formato válido
2. **Codificación Base64**: El contenido HTML debe estar codificado en Base64
3. **Templates**: Los templates se seleccionan automáticamente según el asunto
4. **Adjuntos**: Para prescripciones, el archivo PDF se adjunta automáticamente
5. **Logs**: Todos los envíos se registran en los logs del sistema
6. **AWS SES**: El servicio utiliza Amazon Simple Email Service para el envío

---

## Soporte

Para soporte técnico, contactar al equipo de desarrollo con:
- Logs del error
- Parámetros utilizados en la request
- Código de error recibido

---

**Versión de la API**: 1.3.0  
**Última actualización**: Enero 2024
