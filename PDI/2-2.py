import cv2
import sys
import numpy as np

image = cv2.imread('aurora.jpg', cv2.IMREAD_GRAYSCALE)
if (image is None):
    print("Imagem não encontrada")
    
altura, largura = image.shape

# Obter os quadrantes da imagem original
primeiroQuadrante = image[0:altura//2,0:largura//2]
segundoQuadrante = image[0:altura//2,largura//2:largura]
terceiroQuadrante = image[altura//2:altura,0:largura//2]
quartoQuadrante = image[altura//2:altura,largura//2:largura]

# Criar uma nova imagem com os quadrantes da imagem original trocados
imgTrocada = np.zeros((altura, largura), np.uint8)   
imgTrocada[0:altura//2,0:largura//2] = quartoQuadrante
imgTrocada[0:altura//2,largura//2:largura] = terceiroQuadrante
imgTrocada[altura//2:altura,0:largura//2] = segundoQuadrante
imgTrocada[altura//2:altura,largura//2:largura] = primeiroQuadrante

# Exibir imagem com quadrantes trocados
cv2.namedWindow('Imagem com Quadrantes Trocados', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Imagem com Quadrantes Trocados', imgTrocada)

# Aguardar até que uma tecla seja pressionada
cv2.waitKey(0)
cv2.destroyAllWindows()
