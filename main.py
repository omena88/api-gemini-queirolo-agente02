from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pdfplumber
import tempfile
import os
from typing import Dict
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar los archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

def generate_html_summary(text: str) -> str:
    """
    Genera un resumen en HTML usando OpenAI (modelo gpt-4o)
    """
    print("[LOG] Enviando texto al LLM (OpenAI gpt-4o)...")
    prompt = f"""
    Analiza el siguiente texto de un documento de licitación y genera un resumen estructurado en HTML.
    El resumen debe ser claro y bien organizado, usando clases de Tailwind CSS para el estilo.
    Incluye secciones relevantes como requisitos, experiencia necesaria, documentación requerida, etc.
    
    Texto del documento:
    {text}
    
    Genera el HTML con un diseño moderno y profesional, usando colores corporativos (azul #1E40AF y gris #F3F4F6).
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    html = response.choices[0].message.content
    print("[LOG] Respuesta recibida del LLM (OpenAI gpt-4o).")
    return html

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile) -> Dict[str, str]:
    """
    Endpoint para procesar archivos PDF y extraer requisitos documentales.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        print("[LOG] PDF recibido: ", file.filename)
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            print("[LOG] PDF cargado correctamente en archivo temporal.")
            
            # Extraer texto del PDF usando pdfplumber
            text = ""
            with pdfplumber.open(temp_file.name) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            print("[LOG] Texto extraído del PDF. Longitud:", len(text))
            
            # Eliminar el archivo temporal
            os.unlink(temp_file.name)
            
            # Generar resumen en HTML usando OpenAI gpt-4o
            html_summary = generate_html_summary(text)
            print("[LOG] Proceso completado correctamente. Resumen generado.")
            
            return {"requirements": html_summary}
            
    except Exception as e:
        print("[ERROR] ", str(e))
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}") 