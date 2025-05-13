# Extractor de Requisitos de PDF

Esta aplicación web permite extraer requisitos documentales de archivos PDF de licitaciones.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio o descarga los archivos.

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

1. Inicia el servidor backend:
```bash
python main.py
```
El servidor se iniciará en `http://localhost:8000`

2. Abre el archivo `static/index.html` en tu navegador web.

## Uso

1. En la interfaz web, haz clic en "Seleccionar PDF" para elegir un archivo PDF.
2. Haz clic en "Enviar" para procesar el archivo.
3. Los requisitos documentales extraídos aparecerán en la sección inferior.

## Notas

- La aplicación busca patrones comunes en documentos de licitación para extraer los requisitos.
- En una implementación real, se podría integrar con una API de modelo de lenguaje para mejorar la extracción.
- Los archivos PDF se procesan temporalmente y no se almacenan en el servidor.

## Estructura del Proyecto

```
.
├── main.py              # Backend FastAPI
├── requirements.txt     # Dependencias de Python
├── static/             # Archivos frontend
│   ├── index.html     # Página principal
│   ├── styles.css     # Estilos CSS
│   └── script.js      # JavaScript del cliente
└── README.md          # Este archivo
``` 