import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

class PersonalAgent:
    def __init__(self, profile_path: str, business_path: str):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        try:
            self.db = self._create_vector_db(profile_path, business_path)
            print("DEBUG: Base de datos vectorial (FAISS) creada con éxito.")
        except Exception as e:
            print(f"CRITICAL ERROR creando Vector DB: {e}")
            raise e
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            Eres el asistente virtual de Francisco Vara.
            Usa los siguientes fragmentos de contexto para responder la pregunta del usuario.

            Contexto relevante:
            {context}

            Pregunta: {question}

            Instrucciones:
            1. Actúa como Francisco Vara (tono profesional y cercano).
            2. Explica conceptos complejos de NETV en lenguaje sencillo.
            3. Si la respuesta no está en el contexto, sugiere contactar directamente.
            4. Sé conciso.
            """
        )
        self.chain = (
            {"context": self.db.as_retriever(search_kwargs={"k": 3}), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    def _create_vector_db(self, profile_path: str, business_path: str):
        """Carga archivos, divide en chunks y crea base de datos vectorial."""
        docs = []
        for path in [profile_path, business_path]:
            if os.path.exists(path):
                print(f"DEBUG: Cargando archivo {path}")
                with open(path, "r", encoding="utf-8") as f:
                    docs.append(Document(page_content=f.read(), metadata={"source": path}))
            else:
                print(f"WARNING: Archivo no encontrado {path}")
        
        if not docs:
            raise ValueError("No se encontraron documentos para indexar.")

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        print(f"DEBUG: Documentos divididos en {len(chunks)} fragmentos.")
        
        # Usa FAISS en memoria
        return FAISS.from_documents(chunks, OpenAIEmbeddings())

    def get_response(self, user_message: str) -> str:
        print(f"DEBUG: Generando respuesta para: {user_message}")
        try:
            response = self.chain.invoke(user_message).content
            print(f"DEBUG: Respuesta generada: {response[:50]}...")
            return response
        except Exception as e:
            print(f"ERROR en get_response: {e}")
            return "Lo siento, tuve un problema procesando tu mensaje."

# Uso de ejemplo (para pruebas locales)
if __name__ == "__main__":
    # Rutas absolutas
    PROFILE_PATH = "/Users/vara/IA/NETV/miperfil.md"
    BUSINESS_PATH = "/Users/vara/IA/Agentes/Experimento/netv.md"
    
    agent = PersonalAgent(PROFILE_PATH, BUSINESS_PATH)
    print("Agente NETV inicializado. Escribe 'salir' para terminar.")
    while True:
        msg = input("Cliente: ")
        if msg.lower() == 'salir': break
        answer = agent.get_response(msg)
        print(f"Francisco (IA): {answer}")
