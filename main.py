from fastapi import FastAPI, Form, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from agent import PersonalAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Rutas a los archivos de conocimiento
# Rutas a los archivos de conocimiento (Relativas para Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "miperfil.md")
BUSINESS_PATH = os.path.join(BASE_DIR, "data", "netv.md")

# Inicializar el agente
if os.path.exists(PROFILE_PATH) and os.path.exists(BUSINESS_PATH):
    agent = PersonalAgent(PROFILE_PATH, BUSINESS_PATH)
elif not os.path.exists(PROFILE_PATH):
    print(f"ERROR: No se encontró el archivo de perfil en {PROFILE_PATH}")
    agent = None
elif not os.path.exists(BUSINESS_PATH):
    print(f"ERROR: No se encontró el archivo de negocio en {BUSINESS_PATH}")
    agent = None

@app.post("/whatsapp")
async def reply_whatsapp(Body: str = Form(...)):
    """
    Endpoint para recibir mensajes de WhatsApp vía Twilio.
    Twilio envía los datos como Form Data, por eso usamos Form(...).
    """
    user_message = Body
    print(f"Mensaje recibido: {user_message}")
    
    if not agent:
        return "Error: Agente no inicializado."

    # Generar respuesta con IA
    try:
        response_text = agent.get_response(user_message)
    except Exception as e:
        response_text = "Lo siento, tuve un problema procesando tu mensaje."
        print(f"Error generando respuesta: {e}")

    # Crear respuesta TwiML (XML para Twilio)
    resp = MessagingResponse()
    resp.message(body=response_text)
    
    return Response(content=str(resp), media_type="application/xml")

@app.get("/")
def home():
    return {"status": "online", "service": "Francisco Vara WhatsApp Agent"}
