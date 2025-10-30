import pandas as pd
import requests
import base64
import time
import sys
import re
import logging
import argparse

# --- CONFIGURACIÓN (Actualizada con tus datos) ---
# ¡¡IMPORTANTE!! Asegúrate de que este nombre coincida con tu archivo
ARCHIVO_EXCEL = "Lista.xlsx"
API_URL = "API/URL"
EMAIL_REMITENTE = "noreply@empresa.com" 
PAUSA_SEGUNDOS = 0.2

# Intervalo mínimo entre envíos (segundos). 0.2s => 5 envíos/segundo
MIN_INTERVAL = 0.2

# Timeout para peticiones HTTP
TIMEOUT = 15

# Modo de prueba: si True no se realizarán llamadas reales a la API.
# Para enviar realmente, ejecutar con --send
DRY_RUN = True

# Verificar SSL (poner True en producción si los certificados son válidos)
VERIFY_SSL = False

# Correos para el cuerpo del mensaje
EMAIL_SOPORTE = "soporte@empresa.com"
EMAIL_PERSONAL = "persona@empresa.com"
# ---------------------------------------------------

# --- [NUEVAS PLANTILLAS HTML] ---
# (Formateadas como f-strings para insertar los emails de soporte/personal)
# (Usamos {{nombre_contacto}} como placeholder para el .format() de adentro del bucle)

HTML_1 = f"""
<p>Buenos días,: {{nombre_contacto}}</p>

<p>Estamos verificando que aún se encuentra utilizando el validador anterior para las validaciones.</p>

<p>Queremos corroborar si esto continúa siendo así, ya que dichas herramientas dejarán de estar operativas próximamente.</p>

<p>Recomendamos actualizarse cuanto antes a la nueva plataforma, disponible en el siguiente enlace:<br>
👉 link</p>

<p>Sugerimos efectuar este cambio lo antes posible para evitar interrupciones en la operatoria.</p>

<p><b>Si desean recibir más información o un instructivo de uso,</b> pueden contactar a soporte en {EMAIL_SOPORTE} o responderme directamente a {EMAIL_PERSONAL}.</p>

<p>Este es un correo de aviso informativo.</p>
<br>
<p>Saludos,<br>firma</p>
"""

HTML_2 = f"""
<p>Buenos días,: {{nombre_contacto}}</p>

<p>Estamos verificando que aún se encuentra utilizando el validador anterior para las validaciones.</p>

<p>Queremos corroborar si esto continúa siendo así, ya que dichas herramientas dejarán de estar operativas próximamente.</p>

<p>Recomendamos actualizarse cuanto antes a la nueva plataforma, disponible en el siguiente enlace:<br>
👉 link</p>

<p>Sugerimos efectuar este cambio lo antes posible para evitar interrupciones en la operatoria.</p>

<p><b>Si desean recibir más información o un instructivo de uso,</b> pueden contactar a soporte en {EMAIL_SOPORTE} o responderme directamente a {EMAIL_PERSONAL}.</p>

<p>Este es un correo de aviso informativo.</p>
<br>
<p>Saludos,<br>firma</p>
"""

ASUNTO_1 = "NO RESPONDER A ESTE CORREO Aviso importante – Actualización Sistema 1"
ASUNTO_2 = "NO RESPONDER A ESTE CORREO Aviso importante – Actualización Sistema 2"

# --- FUNCIÓN PRINCIPAL (Ajustada a tu Excel) ---
def enviar_correos(send: bool = False):
    try:
        df = pd.read_excel(ARCHIVO_EXCEL)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{ARCHIVO_EXCEL}'.")
        print("Asegúrate de que el script esté en la misma carpeta que el archivo Excel.")
        return
    except Exception as e:
        print(f"ERROR al leer el Excel: {e}")
        return

    total_correos = len(df)
    logging.info("--- Se encontraron %d correos para procesar ---", total_correos)
    logging.info("API URL: %s", API_URL)
    logging.info("Remitente: %s", EMAIL_REMITENTE)
    if not send or DRY_RUN:
        logging.info("EJECUCIÓN EN MODO DRY RUN (no se harán envíos). Para enviar realmente, ejecute con --send")

    last_send = 0.0
    session = requests.Session()

    for index, fila in df.iterrows():
        try:
            # 1. Obtener datos de la fila (Ajustado a tu Excel)
            email_destino = str(fila.get('contacto_emailAdmin', '')).strip()
            nombre_contacto = fila['nombre_usuario']
            tipo_usuario = fila['Tipo usuario']

            EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if not email_destino or not EMAIL_RE.match(email_destino):
                print(f"Fila {index+1}: email inválido ({email_destino}) — se salta")
                continue

            tipo_usuario_norm = str(fila.get('Tipo usuario', '')).strip().upper()

            # 2. Lógica If/Else para definir el contenido
            if tipo_usuario_norm == '1':
                asunto = ASUNTO_1
                html_body = HTML_1.format(nombre_contacto=nombre_contacto)
            else:
                asunto = ASUNTO_2
                html_body = HTML_2.format(nombre_contacto=nombre_contacto)
            
            # 3. Codificar HTML a Base64 [cite: DOCUMENTACION_API_EMAIL.md]
            html_bytes = html_body.encode('utf-8')
            html_base64 = base64.b64encode(html_bytes).decode('utf-8')

            # 4. Preparar el JSON para la API [cite: DOCUMENTACION_API_EMAIL.md]
            payload = {
                "toEmail": email_destino,
                "fromEmail": EMAIL_REMITENTE,
                "htmlEncoded": html_base64,
                "subject": asunto
            }

            # 5. Llamar a la API (o Dry Run)
            print(f"({index + 1}/{total_correos}) Preparado: {email_destino} -> {asunto}")

            if not send or DRY_RUN:
                print(f"[DRY RUN] No se enviará realmente. Payload to={email_destino} subject={asunto} (html {len(html_base64)} bytes)")
                # respetar rate limit aunque sea dry-run
                now = time.perf_counter()
                elapsed = now - last_send
                if elapsed < MIN_INTERVAL:
                    time.sleep(MIN_INTERVAL - elapsed)
                last_send = time.perf_counter()
                continue

            # Real send: rate limiting
            now = time.perf_counter()
            elapsed = now - last_send
            if elapsed < MIN_INTERVAL:
                time.sleep(MIN_INTERVAL - elapsed)

            # reintentos simples
            max_retries = 2
            sent_ok = False
            for attempt in range(1, max_retries + 1):
                try:
                    response = session.post(API_URL, json=payload, timeout=TIMEOUT, verify=VERIFY_SSL)
                    if response.status_code == 200:
                        print(" ¡Éxito!")
                        sent_ok = True
                        break
                    else:
                        print(f" Intento {attempt}/{max_retries} - ERROR! Código: {response.status_code}, Respuesta: {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f" Intento {attempt}/{max_retries} - EXCEPCIÓN: {e}")
                    time.sleep(1 * attempt)

            if not sent_ok:
                print(f"ERROR: No se pudo enviar a {email_destino} después de {max_retries} intentos.")

            last_send = time.perf_counter()

        except requests.exceptions.RequestException as e:
            print(f"\nERROR DE CONEXIÓN en la fila {index+1}: {e}")
            # continuar con la siguiente fila en lugar de break
            continue
        except Exception as e:
            print(f"\nERROR CRÍTICO en la fila {index + 1} ({email_destino}): {e}")

        # Nota: rate limiting ya controla la cadencia; no se aplica pausa adicional aquí

    print("\n--- Proceso completado. ---")

# --- Ejecutar el script ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enviar correos desde Excel usando API AWS-Sender')
    parser.add_argument('--send', action='store_true', help='Realiza el envío real. Si no se pasa, se ejecuta en DRY RUN')
    parser.add_argument('--file', type=str, help='Archivo Excel a usar (por defecto: ARCHIVO_EXCEL)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    if args.file:
        ARCHIVO_EXCEL = args.file

    if not args.send:
        DRY_RUN = True
    else:
        DRY_RUN = False

    if not VERIFY_SSL:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    enviar_correos(send=args.send)
