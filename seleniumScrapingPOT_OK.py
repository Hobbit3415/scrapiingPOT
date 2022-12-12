# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:44:40 2022

@author: apitto
@author: hobbit3415
"""

<<<<<<< HEAD
# In[01]
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd 
# import wget
=======
# In[]
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Bibliotecas webdriver Firefox
from selenium.webdriver.firefox.options import Options as op_firefox
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Bibliotecas webdriver Chrome
from selenium.webdriver.chrome.options import Options as op_chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import re
from lxml import etree
>>>>>>> testing

# Funciones
os.environ['GH_TOKEN'] = "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"


def normalise(s):
    """
    Metodo que normaliza cadenas de strings que contengan
    caracteres con acentos

    Params:
        s: String a normalizar

    Return:
        String normalizado
    """
    replacements = (
        ("%C3%B3", "ó"),
        ("%C3%A1", "á"),
        ("%C3%AD", "í"),
        ("%C3%B1", "ñ"),
<<<<<<< HEAD
        ('%C3%A9','é'),
        ('%C3%BA','ú')
=======
        ('%C3%A9', 'é'),
        ('%C3%BA', 'ú')
>>>>>>> testing
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def open_driver_firefox(url):
    """
    Metodo que recibe una url y crea un web driver
    al cual se realizará el scraping

    Params:
        url: string

    Return:
        webdriver de Firefox
    """
    options = op_firefox()
    options.add_argument("--disable-notifications")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")

    # Instancia de un webdriver con el servicio de Chrome
    driver = webdriver.Firefox(service=Service(
        GeckoDriverManager().install()), options=options)
    # Abre un navegador de GoogleChrome y carga la URL solicitada
    # Carga por completo todos los scripts del sitio web y descarga
    # el HTML conn el contenido dinamico
    driver.get(url)
    # Duerme el hilo por 10 segundos para asegurarse de que todo el
    # contenido dinamico se cargue completamente
<<<<<<< HEAD
    time.sleep(25)
    # Lista que almacena el contenido de la etiqueta UL
    # XPATH del UL que almacena todos los resultados
    wait = WebDriverWait(driver, 40)
    # driver.implicitly_wait(30)
=======
    time.sleep(6)

    return driver


def open_driver_chrome(url):
    """
    Metodo que recibe una url y crea un web driver
    al cual se realizará el scraping

    Params:
        url: string

    Return:
        webdriver de Chrome
    """
    options = op_chrome()
    options.add_argument("--disable-notifications")
    # options.add_argument("enable-automation")
    # options.add_argument("--headless")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")

    # Instancia de un webdriver con el servicio de Chrome
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    # Abre un navegador de GoogleChrome y carga la URL solicitada
    # Carga por completo todos los scripts del sitio web y descarga
    # el HTML conn el contenido dinamico
    driver.get(url)
    # Duerme el hilo por 10 segundos para asegurarse de que todo el
    # contenido dinamico se cargue completamente
    time.sleep(6)

    return driver


def driver_f(url, xPath):
    """
    Metodo que recibe una url especifica de una pagina web
    en la que se desea buscar un elemento

    Params:
        url: String
        xPath: String que contiene un XPATH de un elemento web HTML

    Return:
        Lista con los web elements encontrados
    """
    driver = open_driver_firefox(url)
    # Lista que almacena el contenido de la etiqueta UL
    # XPATH del UL que almacena todos los resultados
    wait = WebDriverWait(driver, 6)
>>>>>>> testing
    try:
        lista = wait.until(EC.element_to_be_clickable((By.XPATH, xPath)))
        lista.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
<<<<<<< HEAD
        driver_.execute_script("arguments[0].click()", lista)        
    # lista = driver.find_element(By.XPATH, xPath)
    time.sleep(5)
    # Cierra el navegador
    # driver.quit()
=======
        driver_.execute_script("arguments[0].click()", lista)

    time.sleep(5)
>>>>>>> testing
    return lista

url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"


def check_exists_by_xpath(driver, xpath):
    """
    Metodo que verifica que un elemento existe en el sitio
    web que se está consultando

<<<<<<< HEAD
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

# Instancia de un webdriver con el servicio de Chrome
driver_ = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre un navegador de GoogleChrome y carga la URL solicitada
# Carga por completo todos los scripts del sitio web y descarga
# el HTML conn el contenido dinamico
driver_.get(url)
# Duerme el hilo por 10 segundos para asegurarse de que todo el
# contenido dinamico se cargue completamente
time.sleep(10)

wait = WebDriverWait(driver_, 20)

for i in range(0,35):
=======
    Params:
        driver: Elemento de tipo web driver en donde se realizará
        la busqueda del elemento

        xpath: String que contiene un XPATH del elemento a buscar
        en el web driver suministrado

    Return:
        True si el elemento existe
        False si el elemento no existe
    """
>>>>>>> testing
    try:
        # driver.implicitly_wait(6)
        driver.find_element(By.XPATH, xpath)

    except TimeoutException:
        print("Check exist: Timeout Exeption")
        return False

    except NoSuchElementException:
        print("Check exist: El elemento NO existe")
        return False

    print("Check exist: El elemento existe")
    return True


def check_exists_by_css(driver, css):
    """
    Metodo que verifica que un elemento existe en el sitio
    web que se está consultando

    Params:
        driver: Elemento de tipo web driver en donde se realizará
        la busqueda del elemento

        css: String que contiene un Selector CSS del elemento a buscar
        en el web driver suministrado

    Return:
        True si el elemento existe
        False si el elemento no existe
    """
    try:
        driver.find_element(By.CSS_SELECTOR, css)
        driver.implicitly_wait(6)

    except TimeoutException:
        print("Check exist: Timeout Exeption")
        return False

    except NoSuchElementException:
        return False

    print("Check exist: El elemento existe")
    return True


def seekLink(driver, url, xpath):
    """
    Metodo que recibe como parametro un web driver, busca etiquetas
    'a' dentro del mismo y retorna la URL correspondiente a esa etiqueta

    Params:
    driver: Objeto web_driver
    url: String del sito en el que se realizará la busqueda
    xpath: XPATH del elemento a buscar

    Return:
    Enlace: String con el enlace web encontrado dentro del sitio
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    except:
        print("Imposible abrir web driver...")
        driver.close()
        return ""

    if check_exists_by_xpath(driver, xpath):
        print("Scraping link")
        div = driver.find_element(By.XPATH, xpath)
        # print("Elemento encontrado")
        enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')
        # print(div)
        # print(enlace)
        # driver.close()
        return enlace

    elif check_exists_by_xpath(driver, '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[4]/div[2]'):
        # print("Elemento no encontrado")
        print("Intentando con el XPATH con 4")
        # Intentar con el XPATH que tiene el 4
        div = driver.find_element(
            By.XPATH, '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[4]/div[2]')

        enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')

        return enlace

    else:
        print("Enlace no encontrado")
        return ""


def scrap_labels(driver, url, xpath):
    """
    Metodo que busca las etiquetas de un recurso web

    Params:
        driver: Objeto web_driver
        url: String del sito en el que se realizará la busqueda
        xpath: XPATH del elemento a buscar

    Return:
        labels: String que contiene todas las etiquetas encontradas
        y separadas por comas
    """
    # Se ingresa a la url en la que se encuentran las etiquetas
    # driver.get(url)
    # time.sleep(7)
    # Lista que almacena todas etiquetas relacionadas
    # con la pagina
    labels = []
    if check_exists_by_xpath(driver, xpath):
        print("Scraping labels")
        # Se busca el div que contiene las etiquetas
        div = driver.find_element(By.XPATH, xpath)
        # Para cada elemento en el div...
        for element in div.find_elements(By.TAG_NAME, 'li'):
            # Encuentre el objeto con el TAG 'a' y extraiga el texto
            etiqueta = element.find_element(
                By.TAG_NAME, 'a').text

            # Agregue la etiqueta a la lista de etiquetas
            labels.append(etiqueta)

    # Concatene cada label encontrado y separelo por comas
    labels = ",".join(labels)

    return labels


url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"

# In[]
# Estableciendo opciones y creando web driver

# Abre un navegador de Firefox y carga la URL solicitada
# Carga por completo todos los scripts del sitio web y descarga
# el HTML con el contenido dinamico
driver_ = open_driver_firefox(url)

wait = WebDriverWait(driver_, 10)

# In[]
# Clickando boton de showmore
for i in range(0, 19):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ember106"]/button[1]')))
        showmore_link.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver_.execute_script("arguments[0].click()", showmore_link)
    except EC.StaleElementReferenceException:
        print('Botón no encontrado')
<<<<<<< HEAD

# XPATH del UL que almacena todos los resultados
xPath = '//*[@id="search-results"]'

=======


# In[]
# Iniciando variables

# XPATH del UL que almacena todos los resultados
xPath = '//*[@id="search-results"]'

>>>>>>> testing
# Lista que almacena el contenido de la etiqueta UL
listaUl = driver_.find_element(By.XPATH, xPath)

# Lista que almacena el contenido del primer div de cada elemento
# "li". El div tiene como id 'emberXXX' e implementa la clase
# "search-result"
listaLi = listaUl.find_elements(By.CLASS_NAME, "search-result")

# Lista que almacena los enlaces
listaEnlace = []

<<<<<<< HEAD
# Generacion de Dataframe 
names = ['Titulo', 'WebElement']  #Nombres de las columnas
=======
# Generacion de Dataframe
names = ['Titulo', 'Enlace_web', 'Enlace_recursos', 'Etiquetas']
>>>>>>> testing

df = pd.DataFrame()
df = pd.DataFrame(columns=names)

<<<<<<< HEAD
for i in listaLi:
    print('#######################')
    print((normalise(os.path.split(i.find_element(By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-',' '))))
    print (i)
    # Busque el tag "a" e imprima su atributo 'href' (link) buscado
    df2 = pd.DataFrame(columns=names)
    # print(i.find_element(By.TAG_NAME, "a").get_attribute('href'))    
    # Almacenar cada titulo
    df2['Titulo'] = [(normalise(os.path.split(i.find_element(By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-',' ')))]
    df2['WebElement'] = i
    df = df.append(df2, ignore_index=True)
    
# Lista que almacena los valores unicos de los titulos
Titulos_dup = df['Titulo'].duplicated()

names2 = ['Titulo', 'Enlace']  #Nombres de las columnas

df_ = pd.DataFrame()
df_ = pd.DataFrame(columns=names2)

for i in range (62, len(Titulos_dup)):    
    if Titulos_dup[i] == False:
        print(i)
        print(Titulos_dup[i])
        df3 = pd.DataFrame(columns=names2)
        df3['Titulo'] = [df.iloc[i]['Titulo']]
        listaDiv = driver_f((df.iloc[i]['WebElement']).find_element(By.TAG_NAME, "a").get_attribute('href'),'//*[@id="main-region"]/div[1]/div[3]/div[2]')
        df3['Enlace'] = [(listaDiv.find_element(By.TAG_NAME, "a").get_attribute('href'))]
        df_ = df_.append(df3, ignore_index=True)
        
=======
# In[]
# Obteniendo URL de cada sitio web que contiene el recurso buscado
for i in listaLi:
    print('#######################')
    print((normalise(os.path.split(i.find_element(By.TAG_NAME,
          "a").get_attribute('href'))[-1].replace('-', ' '))))
    print(i)
    # Busque el tag "a" e imprima su atributo 'href' (link) buscado
    df2 = pd.DataFrame(columns=names)

    # Almacenar cada titulo
    df2['Titulo'] = [(normalise(os.path.split(i.find_element(
        By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-', ' ')))]
    # Columna en la que se guardan los links del sitio web donde
    # se encuentra el recurso que necesitamos
    df2['Enlace_web'] = i.find_element(By.TAG_NAME, "a").get_attribute('href')
    # df = df.append(df2, ignore_index=True)
    df = pd.concat([df, df2], ignore_index=True)

# In[]
print("\nDataframe hasta el momento")
print(df)

# Ordenar dataset por nombre
# df = df.sort_values(by=["Titulo"])

df.to_clipboard()

# Se cierra el Webdriver de Firefox
driver_.quit()

# In[]
# Se abre un nuevo webdriver pero con Chrome
driver_ = open_driver_chrome(url)

# In[]
# Primeros 4 elementos del df
for i in range(30, len(df)):
    print(f"\n{i}: {df.loc[i, 'Titulo']}")
    # print(i)

    enlace_web = df.iloc[i]['Enlace_web']

    df.to_clipboard()

    link_recurso = seekLink(
        driver_, enlace_web, '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[3]/div[2]')

    if link_recurso != "":
        etiquetas = scrap_labels(
            driver_, enlace_web, "/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[3]/div/div/div[3]/div[3]/ul")

        # Se anexa el enlace al recurso solicitado
    df.loc[i, 'Enlace_recursos'] = link_recurso
    # Se anexa las etiquetas correspondientes a cada recurso
    df.loc[i, 'Etiquetas'] = etiquetas

    print("Elemento agregado a df")


# In[]
df.to_clipboard()


# %%
>>>>>>> testing
