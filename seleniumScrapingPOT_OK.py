# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:44:40 2022

@author: apitto
"""

# In[01]
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException
import time
import os
import pandas as pd
from selenium.webdriver.chrome.options import Options
# import wget

# Funciones


def normalise(s):
    replacements = (
        ("%C3%B3", "ó"),
        ("%C3%A1", "á"),
        ("%C3%AD", "í"),
        ("%C3%B1", "ñ")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def driver_f(url, xPath):
    # Instancia de un webdriver con el servicio de Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Abre un navegador de GoogleChrome y carga la URL solicitada
    # Carga por completo todos los scripts del sitio web y descarga
    # el HTML conn el contenido dinamico
    driver.get(url)

    # Duerme el hilo por 15 segundos para asegurarse de que todo el
    # contenido dinamico se cargue completamente
    time.sleep(15)

    for i in range(0, 2):
        try:
            # Boton de "Mas resultados" guardado en la variable showmore_link
            showmore_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="ember106"]/button[1]')))
            # Click 3 veces en el boton
            showmore_link.click()

        except ElementClickInterceptedException:
            print("Trying to click on the button again")
            driver.execute_script("arguments[0].click()", showmore_link)

        except NoSuchWindowException:
            print(f"****\nBoton click no encontrado:")

    # Lista que almacena el contenido de la etiqueta UL
    # XPATH del UL que almacena todos los resultados
    lista = driver.find_element(By.XPATH, xPath)
    # Cierra el navegador
    return lista


# In[]

options = Options()
options.add_argument("--disable-notifications")

# Instancia de un webdriver con el servicio de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 6)
# Abre un navegador de GoogleChrome y carga la URL solicitada
# Carga por completo todos los scripts del sitio web y descarga
# el HTML conn el contenido dinamico
url = "https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase"
driver.get(url)
# Duerme el hilo por 6 segundos para asegurarse de que todo el
# contenido dinamico se cargue completamente
time.sleep(6)

############
# for i in range(0,int(569/20)+1):
# for i in range(0, 3):
#     try:
#         # Boton de "Mas resultados" guardado en la variable showmore_link
#         showmore_link = wait.until(EC.element_to_be_clickable(
#             (By.XPATH, '//*[@id="ember106"]/button[1]')))
#         # Click 3 veces en el boton
#         showmore_link.click()

#     except ElementClickInterceptedException:
#         print("Trying to click on the button again")
#         driver.execute_script("arguments[0].click()", showmore_link)


# In[]

def extend_links(n_clicks, path):
    for i in range(0, n_clicks):
        try:
            # Boton de "Mas resultados" guardado en la variable showmore_link
            showmore_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, path)))
            # Click 3 veces en el boton
            showmore_link.click()

        except ElementClickInterceptedException:
            print("Trying to click on the button again")
            driver.execute_script("arguments[0].click()", showmore_link)

        # except NoSuchWindowException:
        #     print(f"****\nBoton click no encontrado:")


names = ['Titulo', 'Enlace']  # Nombres de las columnas

df = pd.DataFrame()
df = pd.DataFrame(columns=names)

#######
# URL para objetos de tipo GeoDatabase
listaUl = driver_f(
    'https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase', '//*[@id="search-results"]')

listaLi = listaUl.find_elements(By.CLASS_NAME, "search-result")

# Lista en la que se guardan los links obtenidos
listaLinks = []

# Lista en la que se guardan los titulos
listaTitles = []

# In[]

for i in listaLi[0: 3]:
    # Busque el tag "a" e imprima su atributo 'href' (link) buscado
    df2 = pd.DataFrame(columns=names)
    print(i.find_element(By.TAG_NAME, "a").get_attribute('href'))
    # Extraccion de la cola del link / titulo
    print(os.path.split(i.find_element(By.TAG_NAME,
          "a").get_attribute('href'))[-1].replace('-', ' '))
    # Almacenar cada cola/titulo
    # listaTitles.append(normalise(os.path.split(i.find_element(By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-',' ')))
    df2['Titulo'] = [(normalise(os.path.split(i.find_element(
        By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-', ' ')))]
    # listaTitles.append(normalise(os.path.split(i.find_element(By.TAG_NAME, "a").get_attribute('href'))[-1].replace('-',' ')))
    # ListaDiv contiene la etiqueta "a" con el link a los datos a descargar
    listaDiv = driver_f(i.find_element(By.TAG_NAME, "a").get_attribute(
        'href'), '//*[@id="main-region"]/div[1]/div[3]/div[2]')
    # Almacenar cada link en una lista para realizar scraping a cada uno
    df2['Enlace'] = [(listaDiv.find_element(
        By.TAG_NAME, "a").get_attribute('href'))]
    # listaLinks.append(listaDiv.find_element(By.TAG_NAME, "a").get_attribute('href'))
    # df = df.append(df2, ignore_index=True)
    # Cambio a metodo concat puesto que append se dejara de usar en pandas
    df = pd.concat([df, df2], ignore_index=True)

# %%
df.to_clipboard()

# %%
