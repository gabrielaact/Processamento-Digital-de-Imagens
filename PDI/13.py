import cv2
import numpy as np
import sys

# Carregar a imagem 
image = cv2.imread("digitos-5.png", cv2.IMREAD_UNCHANGED)

if (image is None):
    sys.exit("Imagem não encontrada.")
else:
    # Aplicar a operação de abertura (MORPH_OPEN) na imagem
    # O segundo argumento é o tipo de operação (elemento estruturante retangular 4x10)
    output = cv2.morphologyEx(image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 10)))

    # Exibir o resultado
    cv2.imshow("digitos", output)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

