# Scraping POT
El script presente está diseñado para hacer scraping a los recursos de tipo GeoDatabase del sitio web [Mapas y estadísticas de cundinamarca](https://mapasyestadisticas-cundinamarca-map.opendata.arcgis.com/search?collection=Dataset&type=file%20geodatabase) mediante herramientas para WebDrivers proporcionadas por Selenium

# Requerimientos
Bibliotecas necesarias para ejecutar el script:
* [Selenium](https://pypi.org/project/selenium/)
```
Documentación para Selenium
* https://www.selenium.dev/documentation/overview/
* https://selenium-python.readthedocs.io/
```
* [Webdriver-manager 3.8.5](https://pypi.org/project/webdriver-manager/)
* [Pandas](https://pypi.org/project/pandas/)
* [Time](https://pypi.org/project/python-time/)

# Conceptos importantes
* **XPATH:**
El script hace uso de las etiquetas XPATH para encontrar elementos en un documento HTML.
El siguiente XPATH hace referencia al titulo del primer elemento GeoDatabase del sitio web:

```
/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/ul/li[1]/div/div[2]/div/h3/div/a
```
![image](https://user-images.githubusercontent.com/36966781/207100901-1a210022-faa1-49bc-803e-762a851baac9.png)

De esta forma, se navega entre los elementos que se busca extraer del sitio web

# Como correr el codigo:
El script puede correrse de manera convencional. Sin embargo, es posible correr segmentos del mismo haciendo uso de Visual Studio Code.
Para esto, solo es necesario agregar el comentario ***#In[]*** (Tal como se emplea en el script) o ***#%%***. Esto habilita la función de VS Code
para ejecutar celdas de código. Por ejemplo:

```
print("Saludos desde la celda 1")

print("Saludos desde la celda 2")
```
Al ejecutar este script, el output que se obtendrá será el siguiente:
```
Saludos desde la celda 1
Saludos desde la celda 2
```
Sin embargo, al agregar los comentarios  ***#In[]*** o ***#%%*** y habilitar la ejecución por celdas, es posible ejecutar manualmente una de las dos lineas solamente tal como se muestra en la imagen a continuación:

![Ejecucion por celda](https://user-images.githubusercontent.com/36966781/207107538-42bb152c-099f-4533-a2c1-109691ea457d.gif)

Se recomienda emplear este método de ejecución puesto que permite llevar un mejor control sobre la ejecución del script
