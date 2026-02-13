# Guía de Uso: Agente de WhatsApp con IA

Este agente utiliza tu archivo `miperfil.md` para responder automáticamente mensajes de WhatsApp.

## Requisitos Previos

1.  **Python 3.10+** instalado.
2.  **Cuenta de OpenAI** con saldo (API Key).
3.  **Cuenta de Twilio** (para conectar con WhatsApp real).
4.  **ngrok** (para exponer tu servidor local a internet).

## Instalación

1.  Navega a la carpeta del proyecto:
    ```bash
    cd /Users/vara/IA/Agentes/Experimento/whatsapp_agent
    ```

2.  Crea un entorno virtual e instala dependencias:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  Configura tus claves:
    Crea un archivo `.env` en esta carpeta con tu clave de OpenAI:
    ```
    OPENAI_API_KEY=sk-tu-clave-aqui
    ```

## Ejecución

1.  Inicia el servidor:
    ```bash
    uvicorn main:app --reload
    ```
    El servidor correrá en `http://127.0.0.1:8000`.

2.  Exponlo a internet con ngrok (en otra terminal):
    ```bash
    ngrok http 8000
    ```
    Copia la URL HTTPS que te da ngrok (ej. `https://a1b2c3d4.ngrok.io`).

## Conexión a WhatsApp (Twilio Sandbox)

1.  Ve a tu consola de Twilio > Messaging > Try it out > Send a WhatsApp message.
2.  En "Sandbox Settings", pega tu URL de ngrok en el campo "When a message comes in":
    `https://tu-url-ngrok.ngrok.io/whatsapp`
3.  Guarda los cambios.
4.  Envía un mensaje al número de Sandbox desde tu WhatsApp. ¡El agente responderá!

## Archivos Importantes

*   `main.py`: Servidor web que recibe los mensajes.
*   `agent.py`: Lógica de inteligencia artificial que lee `miperfil.md`.
*   `/Users/vara/IA/NETV/miperfil.md`: Tu base de conocimiento.
