# La asincronía la utilizamos cuando se hacen acciones que implican trabajo externo (I/O que pausan el programa)
# Para no tener que esperar a recolectar todos los datos antes de tratarlos utilizamos los generadores.

from bs4 import BeautifulSoup  #BeautifulSoup nos permite extraer información de contenido en formato HTML o XML
import aiohttp
import asyncio
import requests



def get_images_scr_from_html(html_doc):    #descargar las imagenes de una página HTML
    '''Recupera todo el contenido de los atributos src de las etiquetas img'''
    soup = BeautifulSoup(html_doc, 'html.parser')    #analiza el conjunto de la página
    return (img.get('src') for img in soup.find_all('img'))   #devuelve un generador poruqe hemos cambiado los corchetes por paréntesis como en generaodres.py


'''Ahora queremos cada URI de la imagen a descargar'''
from urllib.parse import urlparse        # Este módulo define una interfaz estándar para dividir las URL en componentes (esquema de direccionamiento, ubicación de red, ruta, etc.), para combinar los componentes nuevamente en una cadena de URL y convertir una 'URL relativa' (versión abreviada de la absoluta) en una 'URL absoluta' dada una 'URL base'.

def get_uri_from_images_src(base_uri, images_src):
    parsed_base = urlparse(base_uri)       #analiza la base del URL. El elemento HTML <base> especifica la dirección URL base que se utilizará para todas las direcciones URL relativas contenidas dentro de un documento. Sólo puede haber un elemento <base> en un documento.

    for src in images_src:
        parsed = urlparse(src)      #analiza el URL de la imagen
        if parsed.netloc == '':
            path = parsed.path      
            if parsed.query:
                path += '?' + parsed.query
    
            elif path[0] != '/':
                if parsed_base.path == '/':
                    path = '/' + path

                else:
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path
                
            yield parsed_base.scheme + '://' + parsed_base.netloc + path    #devolvemos cada resultado en el momento en el que llega
        
        else:
            yield parsed.geturl()     # de nuevo devolvemos cada resultado en el momento en el que llega
     

'''Función que descarga las imágenes y escribe el archivo haciéndolas asíncronas'''
async def main(uri):
    async with aiohttp.ClientSession() as seession:
        s = requests.Session()
        async with s.get(uri) as response:
            if response.status != 200:
                return None
            if response.content_type.startswith('text/'):
                return await response.text()
            else:
                return await response.read()

'''Función wget'''
async def wget(session, uri):
    async with session.get(uri) as response:
        if response.status != 200:
            return None
        if response.content_type.startswith('text/'):
            return await response.text()
        else:
            return await response.read()

'''Función download'''
async def download(session, uri):
    content = await wget(session, uri)
    if content is None:
        return None
    with open(uri.split('/')[-1], 'wb') as f:     #escritura del archivo en el disco duro
        f.write(content)
        return uri

