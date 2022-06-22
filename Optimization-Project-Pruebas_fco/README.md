# Desarrollo Inmobiliario Sustentable (Grupo 65)- ICS1113 2022-1 
# Introducción
El siguiente repositorio contiene el código del proyecto del grupo 65, cuyo tema de trabajo fue el desarrollo inmobiliario sustentable.

Para descargar todo el código, se recomienda clonar el repositorio, para esto utilizar
```sh
git clone https://github.com/panchouc/Desarrollo-Inmobiliario-Sustentable.git
``` 
# Librerías a utilizar
Si bien en el enunciado, se menciona que únicamente se pueden usar 3 librerías (Numpy, Pandas, SymPy), para manejar archivos Excel fue necesario instalar la librería
openpyxl, de lo contrario no se pueden manejar archivos Excel (escritura).

# Instalación de librerías
Para instalar las liberías utilizar el comando (pip o pip3 dependiendo del OS). Se recomienda el uso de un entorno virtual. Para Linux/macOS
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Para crear un entorno virtual, activarlo y descargar las librerías necesarias.
Para Windows

```sh
python -m venv venv
venv/bin/Activate.ps1
pip install -r requirements.txt
```
# Funcionamiento
El archivo que debe ser ejecutado es el main.py. Cerciosarse de estar en el directorio correcto. Para esto ocupar
```sh
cd Optimization-Project/
```
En el archivo grilla.py encontrara las funciones asociadas a la creación de la matriz y lectura de archivo excel.
En el archivo main.py también se encuentran ciertas funciones al inicio del código. Estas no se pudieron traspasar a otro archivo individual, ya que dependen de ciertas variables para poder ejecutarse. 

Se fija una seed en los números random, para así obtener resultados distintos al variar ciertos parámetros, pero no cambiar los números random entre cada iteración.

Para ejecutar el código, solo es necesario ejecutar main.py.
# Resultados
Todos los resultados se encuentran en los archivos .xlsx y .txt. Para visualizar mejor las construcciones, se recomienda que en Excel se seleccione el formato de subrayar los números 2 y 3.

Al momento de ejecutar el modelo se generarán diversos archivos, siendo estos

* matriz_opti.xlsx
* resulta_2.xlsx
* resulta_3.xlsx
* Valor_variables.txt
* variables.txt
* Entrega3.lp
* Entrega3.mps

Donde los archivos .xlsx contienen principalmente una visualización de los edificios construidos y de la grilla que se generó. Los archivos .txt, como dicen, contienen el valor de las variables, en específico, Valor_variables.txt contiene el valor de todas las variables que son distintas de cero. Así, se asume que las
variables que no están presentes en este archivo, toman el valor de cero. Los archivos .lp y .mps contienen información del modelo en forma detallada en caso de querer saber como se ve el modelo específicamente. Mencionar que estos dos archivos son bastante extensos. 

Ciertos valores se imprimirán en consola, como el valor de la función objetivo.
## Autores

* Pedro Palma
* Vicente Pareja
* Felipe Fuentes
* Victoria Hofmann
* Martín Campos
* Francisco Solís