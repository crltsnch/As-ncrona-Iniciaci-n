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
    async for src in images_src:
        parsed = urlparse(src)     #analiza el URI de la imagen
        if parsed.netloc == '':      #.netloc es network location (ubicación de la red), inlcuye el dominio. Si no hay dominio:
            path = parsed.path    #.path contiene información de como se debe acceder al recurso especificado en la URI (ruta)
            if parsed.query:    #.query consultas. Si hay consultas:
                path += '?' + parsed.query   #se añade la consulta a la ruta
            elif path[0] != '/':     #si la ruta no empieza por /
                if parsed_base.path == '/':    #si la ruta de la base es /
                    path = '/' + path      #añadimos la ruta a la ruta base
                else:
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path   #añadimos la rura a la ruta base
                
            yield parsed_base.scheme + '://' + parsed_base.netloc + path    #devolvemos cada resultado en el momento en el que llega
        
        else:  #si hay dominio
            yield parsed.geturl()     #devolvemos la URI de la imagen

        await asyncio.sleep(0.001)   #espera 1 milisegundo


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
    content = await wget(session, uri)   #hacemos la petición
    if content is None:    #si no hay contenido
        return None
    with open(uri.split('/')[-1], 'wb') as f:     #abrimos el archivo
        f.write(content)    #escribimos el contenido
        return uri     #devolvemos la URI



'''Función para descargar las imágenes de una página'''
async def get_images(session, page_uri):
    html = await wget(session, page_uri)   #hacemos una peticion a la página
    if not html:   #si no hay html: error
        print('Error: no se ha encontrado ninguna página', sys.stderr)
        return None
    images_src_gen = get_images_scr_from_html(html)   #obtenemos las imágenes de la página
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)   #obtenemos las URI de las imágenes
    async for image_uri in images_uri_gen:    #recorremos todas las uris de las imágenes
        print('Descarga de %s' % image_uri)   #descarga de (uri de la imagen)
        await download(session, image_uri)   #descargamos la  imagen


'''Funcion principal'''
async def main():
    web_page_uri = 'http://www.formation-python.com/'
    async with aiohttp.ClientSession() as session:  #creamos una sesion para hacer las peticiones
        await get_images(session, web_page_uri)   #descargamos las imágenes


'''Función para escribir en un archivo'''
def write_file(filename, content):
    with open(filename, "wb") as f:    #abrir
        f.write(content)     #reescribir