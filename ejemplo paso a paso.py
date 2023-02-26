# La asincronía la utilizamos cuando se hacen acciones que implican trabajo externo (I/O que pausan el programa)
# Para no tener que esperar a recolectar todos los datos antes de tratarlos utilizamos los generadores.

from bs4 import BeautifulSoup  #BeautifulSoup nos permite extraer información de contenido ne formato HTML o XML

def get_images_scr_from_html(html_doc):    #descargar las imagenes de una pagina HTML
    '''Recupera todo el contenido de los atributos src de las etiquetas img'''
    soup = BeautifulSoup(html_doc, 'html.parser')
