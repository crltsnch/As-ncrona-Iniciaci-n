from bs4 import BeautifulSoup  #BeautifulSoup nos permite extraer información de contenido en formato HTML o XML
from urllib.parse import urlparse        # Este módulo define una interfaz estándar para dividir las URL en componentes (esquema de direccionamiento, ubicación de red, ruta, etc.), para combinar los componentes nuevamente en una cadena de URL y convertir una 'URL relativa' (versión abreviada de la absoluta) en una 'URL absoluta' dada una 'URL base'.
import sys
import time
import requests

'''Función descargar las imágenes de una página HTML'''
'''Cuando se encuentre una imgaen se parsará a la siguiente funcion y se devolverá el control durante una siguiente espera en el programa'''
def get_images_scr_from_html(html_doc):
    '''Recupera todo el contenido de los atributos src de las etiquetas img'''
    soup = BeautifulSoup(html_doc, 'html.parser')    #analiza el conjunto de la página
    return (img.get('src') for img in soup.find_all('img'))  #recuperamos las imágenes de la HTML 


'''Ahora queremos cada URI de cada imagen a descargar'''
'''Se trata de otro generador pero que  trabaja a partir de los resultados del anterior'''
def get_uri_from_images_src(base_uri, images_src):
    parsed_base = urlparse(base_uri)       #analiza la base del URI. El elemento HTML <base> especifica la dirección URL base que se utilizará para todas las direcciones URL relativas contenidas dentro de un documento. Sólo puede haber un elemento <base> en un documento.
    for src in images_src:
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


'''Función wget'''
def wget(uri):
    response = requests.get(uri)    #para hacer una petición al contenido de una URI
    if response.status_code != 200:   #indica el estado de la respuesta, 200 es correcto
        return None
    if response.headers['Content-Type'].startswith('text/'):    #si el tipo de contenido es texto
        return response.text  #devuelve el contenido de la respuesta
    else:    #si no es texto
        return response.content   #devolvemos el contenido de la respuesta



'''Función download'''
def download(uri):
    response = response.get(uri)   #hacemos la petición
    if response.status_code != 200:    #si no hay contenido
        return None
    if response.headers['Content-Type'].startswith('text/'):     #si el tipo de contenido es texto
        return None
    else:
        filename = uri.split('/')[-1]
        with open(filename, 'wb') as f:  #abrimos el fichero
            f.write(response.content)    #escribimos el contenido en el archivo


'''Función para descargar las imágenes de una página'''
def get_images(page_uri):
    html = wget(page_uri)   #hacemos una peticion a la página
    if not html:   #si no hay html: error
        print('Error: no se ha encontrado ninguna imagen', sys.stderr)
        return None
    images_src_gen = get_images_scr_from_html(html)   #obtenemos las imágenes de la página
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)   #obtenemos las URI de las imágenes
    for image_uri in images_uri_gen:    #recorremos todas las uris de las imágenes
        print('Descarga de %s' % image_uri)   #descarga de (uri de la imagen)
        download(image_uri)   #descargamos la  imagen


if __name__ == '__main__':
    #tiempo de ejecucion
    start_time = time.time()
    get_images('http://www.formation-python.com/')
    print("--- El tiempo sin asíncrono es de %s segundos ---" % (time.time() - start_time))