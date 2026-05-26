import requests
from bs4 import BeautifulSoup
import PyPDF2
from docx import Document
import io

def extract_from_url(url: str) -> str:
    """Extrae el texto de una página web, intentando obtener el contenido principal."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar scripts y estilos
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.extract()
            
        # Obtener texto
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        return f"Error al extraer URL: {str(e)}"

def extract_from_pdf(file_bytes: bytes) -> str:
    """Extrae el texto de un archivo PDF."""
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error al leer PDF: {str(e)}"

def extract_from_docx(file_bytes: bytes) -> str:
    """Extrae el texto de un archivo DOCX."""
    try:
        doc_file = io.BytesIO(file_bytes)
        doc = Document(doc_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error al leer DOCX: {str(e)}"
