# La asincronía la utilizamos cuando se hacen acciones que implican trabajo externo (I/O que pausan el programa)
# Para no tener que esperar a recolectar todos los datos antes de tratarlos utilizamos los generadores.

from bs4 import BeautifulSoup  #BeautifulSoup nos permite extraer información de contenido en formato HTML o XML
from urllib.parse import urlparse        # Este módulo define una interfaz estándar para dividir las URL en componentes (esquema de direccionamiento, ubicación de red, ruta, etc.), para combinar los componentes nuevamente en una cadena de URL y convertir una 'URL relativa' (versión abreviada de la absoluta) en una 'URL absoluta' dada una 'URL base'.
import aiohttp
import asyncio
import sys


'''Función descargar las imágenes de una página HTML'''
'''Cuando se encuentre una imgaen se parsará a la siguiente funcion y se devolverá el control durante una siguiente espera en el programa'''
async def get_images_scr_from_html(html_doc):
    '''Recupera todo el contenido de los atributos src de las etiquetas img'''
    soup = BeautifulSoup(html_doc, 'html.parser')    #analiza el conjunto de la página
    for img in soup.find_all('img'):    #busca todas las etiquetas img
        yield img.get('src')    #devuelve cada resultado en el momento en el que llega
        await asyncio.sleep(0.001)    #espera 1 milisegundo



'''Ahora queremos cada URI de cada imagen a descargar'''
'''Se trata de otro generador pero que  trabaja a partir de los resultados del anterior'''
async def get_uri_from_images_src(base_uri, images_src):
    parsed_base = urlparse(base_uri)       #analiza la base del URI. El elemento HTML <base> especifica la dirección URL base que se utilizará para todas las direcciones URL relativas contenidas dentro de un documento. Sólo puede haber un elemento <base> en un documento.
    for src in images_src:
        parsed = urlparse(src)      #analiza el URI de la imagen
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
            yield parsed.geturl()     #devolvemos la URI de la imagen

        asyncio.sleep(0.001) #espera 1 milisegundo


'''Función wget'''
async def wget(session, uri):
    async with session.get(uri) as response:     #para hacer una petición al contenido de una URI
        if response.status != 200:   #indica el estado de la respuesta, 200 es correcto
            return None
        if response.content_type.startswith('text/'):    #si el tipo de contenido es texto
            return await response.text()   #devuelve el contenido de la respuesta
        else:    #si no es texto
            return await response.read()   #esperamos a que se descargue el contenido de la respuesta



'''Función download'''
async def download(session, uri):
    content = await wget(session, uri)
    if content is None:
        return None
    with open(uri.split('/')[-1], 'wb') as f:     #escritura del archivo en el disco duro
        f.write(content)
        return uri



'''Función para descargar las imágenes de una página'''
async def get_images(session, page_uri):
    html = await wget(session, page_uri)
    if not html:
        print('Error: no se ha encontrado ninguna página', sys.stderr)
        return None
    images_src_gen = get_images_scr_from_html(html)
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)
    async for image_uri in images_uri_gen:    #recorremos todas las uris de las imágenes
        print('Descarga de %s' % image_uri)   #descarga del (uri)
        await download(session, image_uri)


'''Funcion principal'''
async def main():
    web_page_uri = 'http://www.formation-python.com/'
    async with aiohttp.ClientSession() as session:
        await get_images(session, web_page_uri)


'''Función para escribir en un archivo'''
def write_file(filename, content):
    with open(filename, "wb") as f:    #abrir
        f.write(content)     #reescribir