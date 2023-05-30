import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import Tk, Button, filedialog, messagebox
import math
from tkinter.ttk import Label

def cerrar_ventana():
    if urlSeguidores != "" or urlSeguidos != "":
        ventana.destroy()
    else:
        messagebox.showinfo(message="Ingrese los archivos correctos", title="Título")


def importar_archivos():
    global urlSeguidos
    global urlSeguidores
    urlSeguidores = ""
    urlSeguidos = ""
    # Abrir el cuadro de diálogo para seleccionar múltiples archivos
    archivos = filedialog.askopenfilenames()

    # Procesar los archivos seleccionados
    for archivo in archivos:
        if("followers" in archivo):
            urlSeguidores = str(archivo)
        if("following" in archivo):
            urlSeguidos = str(archivo)

# Crear la ventana principal
ventana = Tk()

label_info = Label(text = "Seleccione los archivos <IG-#######following.csv> y <IG-#######followers.csv>")
label_info.pack()
# Crear el botón de importar archivos
boton_importar = Button(ventana, text="Importar archivos", command=importar_archivos)
boton_importar.pack()

# Crear el botón de agregar los archivos
boton_cerrar = Button(ventana, text="Aceptar", command=cerrar_ventana)
boton_cerrar.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()


# Leer el archivo CSV
dataSeguidores = pd.read_csv(urlSeguidores)
dataSeguidos = pd.read_csv(urlSeguidos)

# Obtener el vector a partir de una columna específica
vectorSeguidores = np.array(dataSeguidores['userName'])
vectorSeguidos = np.array(dataSeguidos['userName'])
vectorSeguidosUrl = np.array(dataSeguidos['avatarUrl'])
noMeSuiguenUsuarios = []
noMeSuiguenUrl = []
for userSeguidos, url in zip(vectorSeguidos, vectorSeguidosUrl):
    teSigue = False
    for userSeguidores in vectorSeguidores:
        if userSeguidos == userSeguidores:
            teSigue = True
    if not teSigue:
        noMeSuiguenUsuarios.append(userSeguidos)
        noMeSuiguenUrl.append(url)

cantidad = len(noMeSuiguenUrl)
print("No te siguen: " + str(cantidad) + " personas")

elementosPorPag = 25

paginas = cantidad/elementosPorPag
paginaActual = 1
inicioNmrImagen = 0

while paginaActual <= math.ceil(paginas):
    print("inicio " + str(inicioNmrImagen))
    if paginaActual == math.ceil(paginas):
        finNmrIgamen = cantidad - 1
    else:
        finNmrIgamen = (paginaActual * elementosPorPag) - 1
    print("fin " + str(finNmrIgamen))

    # Descargar las imágenes y almacenarlas en una lista
    imagenes = []
    x = inicioNmrImagen
    contadorFor = 0
    for url in noMeSuiguenUrl:
        if contadorFor >= x:
            response = requests.get(url)
            imagen = Image.open(BytesIO(response.content))
            imagenes.append(imagen)
            x += 1
        if x > finNmrIgamen:
            break
        contadorFor+=1

    # Crear una figura y subgráficos
    num_imagenes = len(imagenes)

    #fig, axs = plt.subplots(1, num_imagenes)
    fig, axs = plt.subplots(5, 5, sharex='col', sharey='row')

    # Mostrar las imágenes con texto en los subgráficos
    y = inicioNmrImagen
    """for i, imagen in enumerate(imagenes):
        axs[i].imshow(imagen)
        axs[i].axis('off')
        axs[i].text(0.5, -0.9, noMeSuiguenUsuarios[y], transform=axs[i].transAxes,
                    fontsize=5, ha='center')
        y+=1"""

    z = 0
    for row in range(5):
        for col in range(5):
            axs[row, col].axis('off')
            if y < cantidad:
                axs[row, col].imshow(imagenes[z])
                axs[row, col].text(0.5, -0.15, noMeSuiguenUsuarios[y], transform=axs[row, col].transAxes,
                        fontsize=6, ha='center')
            y += 1
            z += 1
    plt.show()

    inicioNmrImagen = finNmrIgamen + 1

    paginaActual += 1