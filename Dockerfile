# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias primero
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto 8000 para FastAPI
EXPOSE 8000

# Comando recomendado para producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 