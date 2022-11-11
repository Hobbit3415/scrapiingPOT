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
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from webdriver_manager.chrome import ChromeDriverManager

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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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


url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"

url_individual = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/datasets/cartografia-basica-municipio-de-gachancip%C3%A1-escala-1k-2020-gdb/about"

# In[]
# Probando individualemente enlace que da problemas

# url_individual = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/datasets/cartografia-basica-municipio-de-gachancip%C3%A1-escala-1k-2020-gdb/about"

# driver_ = webdriver.Chrome(service=Service(
#     ChromeDriverManager().install()))

# driver_.get(url_individual)

# time.sleep(6)

# # wait = WebDriverWait(driver_, 40)

# elemento = driver_.find_element(
#     By.XPATH, '//*[@id="main-region"]/div[1]/div[4]/div[2]').find_element(By.TAG_NAME, "a").get_attribute('href')

# print(elemento)


# In[]
# Estableciendo opciones y creando web driver
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
# options.add_argument("--disable-gpu")

# Instancia de un webdriver con el servicio de Chrome
driver_ = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

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

# Celda para copiar df a portapapeles y visualizarlos mejor en excel
# print(Titulos_dup)
# print(df)
# Titulos_dup.to_clipboard()

# df.to_clipboard()
# In[]


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

    div = driver.find_element(By.XPATH, xpath)

    enlace = div.find_element(By.TAG_NAME, "a").get_attribute('href')

    print(div)
    print(enlace)

    # a_locator = driver.find_elements(locate_with(By.TAG_NAME, 'a').below(div))

    # enlace = a_locator.find_element(By.TAG_NAME, "a").get_attribute('href')

    # print("Encontrado: \n{}\n{}".format(titulo, enlace))
    # return enlace


# In[]
for i in range(62, len(Titulos_dup)):
    if Titulos_dup[i] == False:
        print(i)
        print(Titulos_dup[i])
        df3 = pd.DataFrame(columns=names2)
        df3['Titulo'] = [df.iloc[i]['Titulo']]
        # df3['Enlace'] = seekLink(df.iloc[i]["WebElement"])
        seekLink(df.iloc[i]["WebElement"],
                 '//*[@id="main-region"]/div[1]/div[3]/div[2]')

        # listaDiv = driver_f((df.iloc[i]['WebElement']).find_element(
        #     By.TAG_NAME, "a").get_attribute('href'), '//*[@id="main-region"]/div[1]/div[3]/div[2]')

        # listaDiv = driver_f((df.iloc[i]['WebElement']).find_element(
        #         By.TAG_NAME, "a").get_attribute('href'), '//*[@id="main-region"]/div[1]/div[4]/div[2]')

        # df3['Enlace'] = [(listaDiv.find_element(
        #     By.TAG_NAME, "a").get_attribute('href'))]
        # # df_ = df_.append(df3, ignore_index=True)
        df_ = pd.concat([df_, df3], ignore_index=True)

# %%
