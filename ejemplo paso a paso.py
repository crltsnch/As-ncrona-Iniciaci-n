# La asincronía la utilizamos cuando se hacen acciones que implican trabajo externo (I/O que pausan el programa)
# Para no tener que esperar a recolectar todos los datos antes de tratarlos utilizamos los generadores.

from bs4 import BeautifulSoup  #BeautifulSoup nos permite extraer información de contenido en formato HTML o XML

def get_images_scr_from_html(html_doc):    #descargar las imagenes de una pagina HTML
    '''Recupera todo el contenido de los atributos src de las etiquetas img'''
    soup = BeautifulSoup(html_doc, 'html.parser')
    return (img.get('src') for img in soup.find_all('img'))   #devuelve un generador poruqe hemos cambiado los corchetes por paréntesis como en generaodres.py


'''Ahora queremos cada URI de la imagen a descargar'''
def get_uri_from_images_src(base_uri, images_src):
    parsed_base = urlparse(base_uri)
    