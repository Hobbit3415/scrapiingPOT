# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:44:40 2022

@author: apitto
"""

# In[]
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

# Funciones
os.environ['GH_TOKEN'] = ""


def normalise(s):
    replacements = (
        ("%C3%B3", "ó"),
        ("%C3%A1", "á"),
        ("%C3%AD", "í"),
        ("%C3%B1", "ñ"),
        ('%C3%A9', 'é'),
        ('%C3%BA', 'ú')
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def open_driver(url):

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=600,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")

    # Instancia de un webdriver con el servicio de Chrome
    # driver = webdriver.Firefox(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=Service(
        GeckoDriverManager().install()), options=options)
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

    Retorna un Web element
    """
    driver = open_driver(url)
    # Lista que almacena el contenido de la etiqueta UL
    # XPATH del UL que almacena todos los resultados
    wait = WebDriverWait(driver, 6)
    # driver.implicitly_wait(30)
    try:
        lista = wait.until(EC.element_to_be_clickable((By.XPATH, xPath)))
        lista.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver_.execute_script("arguments[0].click()", lista)
    # lista = driver.find_element(By.XPATH, xPath)
    time.sleep(5)
    # Cierra el navegador
    # driver.quit()
    return lista


def check_exists_by_xpath(driver, xpath):
    """
    Metodo que recibe como aprametro un XPATH a buscar

    Return:
        True si el elemento existe
        False si el elemento no existe
    """
    try:
        driver.find_element(By.XPATH, xpath)
        driver.implicitly_wait(6)

    except NoSuchElementException:
        return False

    return True


def seekLink(url, xpath):
    """
    Metodo que recibe como parametro un web element, busca etiquetas
    'a' dentro del mismo y retorna la URL correspondiente a esa etiqueta

    Params:
    web_element : URL de sitio web
    """

    driver = open_driver(url)

    if check_exists_by_xpath(driver, xpath):
        div = driver.find_element(By.XPATH, xpath)
        print("Elemento encontrado")
        enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')
        print(div)
        print(enlace)
        driver.close()
        return enlace

    else:
        print("Elemento no encontrado")
        print("Intentando con el XPATH con 4")
        # Intentar con el XPATH que tiene el 4
        div = driver.find_element(
            By.XPATH, '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[4]/div[2]')
        enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')

        print(div)
        print(enlace)
        driver.close()
        return enlace


url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"

# In[]
# Estableciendo opciones y creando web driver

# Abre un navegador de GoogleChrome y carga la URL solicitada
# Carga por completo todos los scripts del sitio web y descarga
# el HTML conn el contenido dinamico
driver_ = open_driver(url)

wait = WebDriverWait(driver_, 10)

# In[]
# Clickando boton de showmore
for i in range(0, 35):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ember106"]/button[1]')))
        showmore_link.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver_.execute_script("arguments[0].click()", showmore_link)
    except EC.StaleElementReferenceException:
        print('Botón no encontrado')

# In[]
# Iniciando variables

# XPATH del UL que almacena todos los resultados
xPath = '//*[@id="search-results"]'

# Lista que almacena el contenido de la etiqueta UL
listaUl = driver_.find_element(By.XPATH, xPath)

# Lista que almacena el contenido del primer div de cada elemento
# "li". El div tiene como id 'emberXXX' e implementa la clase
# "search-result"
listaLi = listaUl.find_elements(By.CLASS_NAME, "search-result")

# Lista que almacena los enlaces
listaEnlace = []

# Generacion de Dataframe
names = ['Titulo', 'Enlace_web', 'Enlace_recursos']

df = pd.DataFrame()
df = pd.DataFrame(columns=names)

# In[]
# Obteniendo URL de cada elemento individual

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
df.to_clipboard()

# Cerrar el driver para no consumir mas RAM
driver_.close()

# In[]

for i in range(41, df.shape[0]):
    print(i)
    print(df.iloc[i])
    # df = pd.DataFrame(columns=names)
    # df['Titulo'] = [df.iloc[i]['Titulo']]
    df["Enlace_recursos"] = seekLink(df.iloc[i]['Enlace_web'],
                                     '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[3]/div[2]')

    print("Elemento agregado a df")
    # df = pd.concat([df, df3], ignore_index=True)

# In[]
df.to_clipboard()

# %%
