import cv2
import numpy as np

# Carregar a imagem em escala de cinza
original = cv2.imread("bolhas.png", cv2.IMREAD_GRAYSCALE)

# Verificar se a imagem foi carregada com sucesso
if original is None:
    print("Deu ruim")
else:
    image = original.copy()
    p = (0, 0)
    n_com_furos = 0
    n_sem_furos = 0

    # Retirar as bolhas que estejam nas bordas
    for i in range(image.shape[0]):
        # Borda esquerda
        if image[i, 0] == 255:
            p = (0, i)
            cv2.floodFill(image, None, p, 0)
        # Borda direita
        if image[i, -1] == 255:
            p = (image.shape[1] - 1, i)
            cv2.floodFill(image, None, p, 0)

    for i in range(image.shape[1]):
        # Borda superior
        if image[0, i] == 255:
            p = (i, 0)
            cv2.floodFill(image, None, p, 0)
        # Borda inferior
        if image[-1, i] == 255:
            p = (i, image.shape[0] - 1)
            cv2.floodFill(image, None, p, 0)

    # Preencher fundo com cor diferente
    p = (0, 0)
    cv2.floodFill(image, None, p, 1)

    # Bolhas com 1 furo ou mais
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 0 and image[i - 1, j - 1] == 255:
                n_com_furos += 1

                p = (j - 1, i - 1)
                cv2.floodFill(image, None, p, 80)

                p = (j, i)
                cv2.floodFill(image, None, p, 128)

            # Furos dentro de bolhas já contadas
            if image[i, j] == 255 and image[i - 1, j - 1] == 128:
                p = (j, i)
                cv2.floodFill(image, None, p, 180)

    # Bolhas sem furos
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 255:
                n_sem_furos += 1
                p = (j, i)
                cv2.floodFill(image, None, p, 254)
    
    total = n_com_furos + n_sem_furos

    print("Bolhas com furos:", n_com_furos)
    print("Bolhas sem furos:", n_sem_furos)
    print("Total:", total) 

    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

