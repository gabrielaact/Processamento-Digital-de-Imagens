from typing import Match
import numpy as np
import sys
import cv2

# Criar funções para auxiliar no código
class Filtros:
    media = np.array([[0.1111, 0.1111, 0.1111],
                      [0.1111, 0.1111, 0.1111],
                      [0.1111, 0.1111, 0.1111]],dtype=np.float32)
    gauss = np.array([[0.0625,0.125,0.0625],
                      [0.125, 0.25,0.125],
                      [0.0625, 0.125,  0.0625]],dtype=np.float32)
    horizontal = np.array([[-1,0,1],
                           [-2,0,2],
                           [-1,0,1]],dtype=np.float32)
    vertical = np.array([[-1,-2,-1],
                         [0,0,0],
                         [1,2,1]],dtype=np.float32)
    laplace = np.array([[0,-1,0],
                        [-1,4,-1],
                        [0,-1,0]],dtype=np.float32)
    boost = np.array([[0, -1, 0],
                      [-1, 5.2, -1],
                      [0, -1, 0]],dtype=np.float32)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sys.exit("Não foi possível abrir a câmera.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

absolute = True
doLaplacian = False
mask = Filtros.media

print('Filtragem Media escolhida como padrão')
print("\Press the key correspondent to the filter: \n"
        "a - abs\n"
        "m - mean\n"
        "g - gauss\n"
        "v - vertical\n"
        "h - horizontal\n"
        "l - laplacian\n"
        "b - boost\n"
        "p - gaussian laplacian\n"
        "esc - quit\n")

while True:
    # Capturar frame por frame
    ret, frame = cap.read()
    # Verificar se o frame foi aberto
    if not ret:
        print("Imagem não encontrada.")
        break

    # Trasformar a imagem recebida em escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imageFloat32 = np.array(gray, dtype=np.float32)
    
    # Realizar a filtragem escolhida
    imgFiltrada = cv2.filter2D(imageFloat32,-1,mask, anchor=(1,1))
    
    if(doLaplacian):
        mask = Filtros.laplace
        imgLaplGaussFiltrada = cv2.filter2D(imgFiltrada,-1,mask, anchor=(1,1))
 
        if absolute:
            imgLaplGaussFiltrada = abs(imgLaplGaussFiltrada)
            
        result = np.array(imgLaplGaussFiltrada, dtype=np.uint8)
        
        res = np.hstack((gray, result))
        cv2.imshow('Filtrando', res)
        
        mask = Filtros.gauss
    else:
        if absolute:
            imgFiltrada = abs(imgFiltrada)
    
        result = np.array(imgFiltrada, dtype=np.uint8)
       
        res = np.hstack((gray, result))
        cv2.imshow('Filtrando', res)
    
    key = cv2.waitKey(10)
    if(key == 27):
        break
    elif(key == ord('a')):
        print('abs modificado')
        absolute = not absolute
    elif(key == ord('m')):
        doLaplacian = False
        print('media escolhida')
        mask = Filtros.media
        print(mask)
    elif(key == ord('g')):
        doLaplacian = False
        print('Gauss escolhida')
        mask = Filtros.gauss
        print(mask)
    elif(key == ord('l')):
        doLaplacian = False
        print('Laplacian escolhida')
        mask = Filtros.laplace
        print(mask)
    elif(key == ord('h')):
        doLaplacian = False
        print('Horizontal escolhida')
        mask = Filtros.horizontal
        print(mask)
    elif(key == ord('v')):
        doLaplacian = False
        print('Vertical escolhida')
        mask = Filtros.vertical
    elif(key == ord('b')):
        doLaplacian = False
        print('Boost escolhida')
        mask = Filtros.boost
        print(mask)
    elif(key == ord('p')):
        print('Laplacian Gauss escolhida')
        mask = Filtros.gauss
        print(mask, '/n', Filtros.laplace)
        doLaplacian = True
        
cap.release()
cv2.destroyAllWindows()
