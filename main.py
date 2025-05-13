from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import tempfile
import os
from typing import Dict

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_documentary_requirements_from_text(pdf_text: str) -> str:
    """
    Función que simula la extracción de requisitos documentales del texto del PDF.
    En una implementación real, esta función se conectaría a una API de LLM.
    """
    # Palabras clave comunes en documentos de licitación
    keywords = [
        "REQUISITOS DEL PROVEEDOR",
        "PERFIL DEL CONSULTOR",
        "EXPERIENCIA MÍNIMA DEL POSTOR",
        "Acreditación:",
        "Requisitos:",
        "Documentación:",
        "Experiencia:",
        "Capacidad técnica:"
    ]
    
    requirements = []
    lines = pdf_text.split('\n')
    
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                # Extraer el párrafo o lista que sigue a la palabra clave
                current_requirement = [line]
                j = i + 1
                while j < len(lines) and lines[j].strip() and not any(k.lower() in lines[j].lower() for k in keywords):
                    current_requirement.append(lines[j])
                    j += 1
                requirements.append('\n'.join(current_requirement))
    
    if not requirements:
        return "No se encontraron requisitos documentales en el PDF."
    
    return "\n\n".join(requirements)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile) -> Dict[str, str]:
    """
    Endpoint para procesar archivos PDF y extraer requisitos documentales.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Extraer texto del PDF usando pdfplumber
            text = ""
            with pdfplumber.open(temp_file.name) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            # Eliminar el archivo temporal
            os.unlink(temp_file.name)
            
            # Extraer requisitos
            requirements = extract_documentary_requirements_from_text(text)
            
            return {"requirements": requirements}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 