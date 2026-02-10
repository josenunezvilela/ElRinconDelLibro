import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def buscar_libros_lista(consulta):
    """Devuelve una lista con los 10 primeros resultados (ID, Título, Autor)."""
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": consulta, "maxResults": 10, "langRestrict": "es"
    }
    if GOOGLE_API_KEY:
        params['key'] = GOOGLE_API_KEY
    try:
        print(f"Buscando: {consulta}...")
        response = requests.get(url, params=params)
        response.raise_for_status() 
        datos = response.json()
        resultados=[]
        
        if "items" in datos:
            for item in datos["items"]:
                info= item.get("volumeInfo",{})
                resultados.append({
                    "id": item["id"],
                    "titulo": info.get("title", "Sin título"),
                    "autor": ", ".join(info.get("authors", ["Desc."]))
                })
        return resultados
    except Exception as e:
        # Cualquier otro error genérico
        print(f"Error desconocido: {e}")
        return "🐛 Ocurrió un error inesperado al procesar el libro."
    

def obtener_detalle_libro(google_id):
    """Busca unn libro específico por su ID y devuelve la descripción completa"""
    url=f"https://www.googleapis.com/books/v1/volumes/{google_id}"
    params={}
    
    if GOOGLE_API_KEY:
        params['key'] = GOOGLE_API_KEY
        
    try:
        response=requests.get(url)
        datos=response.json()
        info=datos.get("volumeInfo",{})
        
        titulo = info.get("title", "Sin título")
        desc = info.get("description", "Sin descripción disponible.")
        paginas = info.get("pageCount", "?")
        
        # Limpiamos un poco el texto
        if len(desc) > 800: desc = desc[:800] + "..."
        
        return f"📖 *{titulo}*\n📄 Páginas: {paginas}\n\n📝 *Sinopsis:*\n{desc}"
    except Exception:
        return "❌ Error al obtener los detalles."