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
agent = None
startup_error = None

try:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is missing!")

    if os.path.exists(PROFILE_PATH) and os.path.exists(BUSINESS_PATH):
        print(f"DEBUG: Loading agent with profiles: {PROFILE_PATH}, {BUSINESS_PATH}")
        agent = PersonalAgent(PROFILE_PATH, BUSINESS_PATH)
    else:
        missing = []
        if not os.path.exists(PROFILE_PATH): missing.append(PROFILE_PATH)
        if not os.path.exists(BUSINESS_PATH): missing.append(BUSINESS_PATH)
        startup_error = f"Missing knowledge files: {', '.join(missing)}"
        print(f"ERROR: {startup_error}")

except Exception as e:
    startup_error = str(e)
    print(f"CRITICAL STARTUP ERROR: {e}")

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
    status = "online" if agent else "offline"
    return {
        "status": status, 
        "service": "Francisco Vara WhatsApp Agent",
        "error": startup_error
    }
