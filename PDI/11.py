import numpy as np
import sys
import cv2
import random

# Variaveis globais
top_slider = 100;

# Aplica o filtro de Canny na imagem 
def filtroCanny(img):
    global top_slider, imgCanny
    imgCanny = cv2.Canny(img,top_slider, 3*top_slider)
    return imgCanny


# Cria uma imagem em Pontilhimos
def pontilhismo(img):
    height, width = img.shape
    
    # Pega o valor do raio aleatório
    radius = random.randint(1, 5)
    
    # Cria uma copia da imagem
    imgCopy = img.copy() 
    
    # Interação para criar os circulos aletoriamente
    for i in range(0,height,radius):
        for j in range(0,width,radius):
            number = random.randint(0, 1)
            if number == 1:
                # Pega a cor do pixel no ponto da matriz
                gray = int(img[i][j])
                color = (gray,gray,gray)
                # Cria um circulo com o raio encontrado aleatoriamente
                cv2.circle(imgCopy, (j,i), radius, color, radius)
                # Pega um novo valor para o raio
                radius = random.randint(1, 5)
    
    return imgCopy
            
# Carregar a imagem
img = cv2.imread("aurora.jpg", cv2.IMREAD_GRAYSCALE)

if (img is None):
    sys.exit("Imagem não encontrada.")
    
# Obter as dimensões da imagem
height, width = img.shape

cv2.imshow("Original", img)

# Aplicar o filtro Canny na imagem
imgCanny = filtroCanny(img)
cv2.imshow("Canny", imgCanny)

# Aplicar o pontilhismo na imagem
imgPonti = pontilhismo(img)
cv2.imshow("pontilhismo", imgPonti)

# Aplicar Canny com Pontilhismo
heightPonti, widthPonti = imgPonti.shape
radius = 4 

imgCannyPoint = imgPonti.copy()

for i in range(heightPonti):
    for j in range(widthPonti):
        if (imgCanny[i][j] == 255):
            gray = int(img[i][j])
            color = (gray, gray, gray)
            cv2.circle(imgCannyPoint, (j, i), radius, color, radius)

cv2.imshow("cannypoint", imgCannyPoint)

cv2.waitKey(0)
cv2.destroyAllWindows()
