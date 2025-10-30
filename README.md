# Automatización de Envíos por Email

Proyecto pequeño para enviar correos masivos desde archivos Excel usando una API REST.

## Características

- Lectura de destinatarios desde archivos Excel
- Envío de correos personalizados según tipo de usuario
- Control de velocidad (rate limiting) configurable
- Reintentos automáticos en caso de fallo
- Modo dry-run (pruebas sin envío real)
- Plantillas HTML personalizables

## Requisitos

- Python 3.x
- Dependencias: `pandas`, `requests`

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:

```bash
pip install pandas requests
```

## Uso

El script principal acepta los siguientes argumentos:

```bash
python enviadorMails.py [--send] [--file ARCHIVO_EXCEL]
```

Argumentos:

- `--send`: Realiza el envío real. Sin este argumento, el script hace un dry-run.
- `--file`: Archivo Excel a procesar (opcional).

### Ejemplo

```bash
# Dry-run (sin enviar)
python enviadorMails.py

# Envío real usando archivo específico
python enviadorMails.py --send --file lista_contactos.xlsx
```

## Estructura del proyecto

```
.
├── enviadorMails.py                 # Script principal
├── README.md                        # Documentación general
```

## Configuración

Los parámetros principales se encuentran en la cabecera de `enviadorMails.py`:

- Rate limiting (pausas entre envíos)
- Timeouts de conexión
- URL de la API
- Configuración SSL

## Manejo de errores

El script incluye:

- Validación básica de emails
- Reintentos automáticos
- Mensajes de logging en consola

## Mantenimiento

1. Mantener las plantillas HTML actualizadas.
2. Probar en dry-run antes de cualquier envío masivo.
3. Versionar cambios y mantener documentación en `docs/`.

---
Proyecto-ITC-soluciones




