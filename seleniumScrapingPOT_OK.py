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

# import wget

# Funciones


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
    # Instancia de un webdriver con el servicio de Chrome
    # driver = webdriver.Firefox(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    # Abre un navegador de GoogleChrome y carga la URL solicitada
    # Carga por completo todos los scripts del sitio web y descarga
    # el HTML conn el contenido dinamico
    driver.get(url)
    # Duerme el hilo por 10 segundos para asegurarse de que todo el
    # contenido dinamico se cargue completamente
    time.sleep(10)

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
    wait = WebDriverWait(driver, 20)
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

        # wait = WebDriverWait(driver, timeout=7)
        # wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

        driver.find_element(By.XPATH, xpath)
        # if len(driver.find_elements(By.XPATH, xpath)) > 0:
        # return True
        # else:
        #     return False
        # wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        driver.implicitly_wait(6)

    except NoSuchElementException:
        return False

    return True


def seekLink(web_element, xpath):
    """
    Metodo que recibe como parametro un web element, busca etiquetas
    'a' dentro del mismo y retorna la URL correspondiente a esa etiqueta

    Params:
    web_element : Tipo web_element
    """

    link_pagina = web_element.find_element(
        By.TAG_NAME, "a").get_attribute('href')

    driver = open_driver(link_pagina)

    if check_exists_by_xpath(driver, xpath):
        div = driver.find_element(By.XPATH, xpath)
        enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')

        print(div)
        print(enlace)

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


url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"

url_individual = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/datasets/cartografia-basica-municipio-de-gachancip%C3%A1-escala-1k-2020-gdb/about"


# In[]
# Estableciendo opciones y creando web driver
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=800,600")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
# options.add_argument("--disable-gpu")

driver_ = webdriver.Firefox(service=Service(
    GeckoDriverManager().install()), options=options)

# Abre un navegador de GoogleChrome y carga la URL solicitada
# Carga por completo todos los scripts del sitio web y descarga
# el HTML conn el contenido dinamico
driver_.get(url)
# Duerme el hilo por 10 segundos para asegurarse de que todo el
# contenido dinamico se cargue completamente
time.sleep(10)

wait = WebDriverWait(driver_, 20)

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
names = ['Titulo', 'WebElement']  # Nombres de las columnas

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
    # print(i.find_element(By.TAG_NAME, "a").get_attribute('href'))
    # Almacenar cada titulo
    df2['Titulo'] = [(normalise(os.path.split(i.find_element(
        By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-', ' ')))]
    df2['WebElement'] = i
    # df = df.append(df2, ignore_index=True)
    df = pd.concat([df, df2], ignore_index=True)

# Lista que almacena los valores unicos de los titulos
Titulos_dup = df['Titulo'].duplicated()

names2 = ['Titulo', 'Enlace']  # Nombres de las columnas

df_ = pd.DataFrame()
df_ = pd.DataFrame(columns=names2)

# In[]
for i in range(0, len(Titulos_dup)):
    if Titulos_dup[i] == False:
        print(i)
        print(Titulos_dup[i])
        df3 = pd.DataFrame(columns=names2)
        df3['Titulo'] = [df.iloc[i]['Titulo']]
        df3["Enlace"] = seekLink(df.iloc[i]["WebElement"],
                                 '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div[1]/div[3]/div[2]')

        df_ = pd.concat([df_, df3], ignore_index=True)

# In[]
df.to_clipboard()

# %%
