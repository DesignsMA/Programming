from PIL import Image
import numpy as np
import sys
def imageToBinary(file):
    # Cargar imagen en escala de grises para simplificar
    img = Image.open(file).convert("L")   #convierte a escala de grises
    img = img.resize((128,128))
    #convierte la imagen en un array NumPy, donde cada elemento representa el valor de un píxel.
    # una imagen de 3x3 devuelve:
    #array([[ 50, 120, 200],
    #       [255, 180, 90],
    #       [ 30,  60, 150]])
    
    pixel_array = np.array(img)
    # Convertir cada píxel en binario
    # Abrir el archivo de salida en modo escritura
    with open("bin.txt", 'w') as f:
        # Iterar a través de todas las filas de la imagen
        for i in range(pixel_array.shape[0]):
            # Iterar a través de todas las columnas de la imagen
            for j in range(pixel_array.shape[1]):
                # Comparar el valor del píxel con el umbral de 128
                if pixel_array[i, j] > 128:
                    f.write('1')
                else:
                    f.write('0')

            # Después de escribir todos los píxeles de la fila, agregar un salto de línea
            f.write('\n')    
    print(pixel_array)
    return pixel_array

if len(sys.argv) < 2:
    print("Error.")
else:
    imageToBinary(sys.argv[1])
    