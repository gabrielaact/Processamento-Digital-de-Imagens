import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sys.exit("Não conseguimos abrir a câmera.")

# Seto a largura e altura da janela de video
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

# Configura plotagem do Gráfico de Histograma
fig, ax = plt.subplots()
ax.set_title('Histogram (grayscale)')
ax.set_xlabel('Itensidade do Vermelho')
ax.set_ylabel('Frequência do Vermelho')
lineVer, = ax.plot(np.arange(256),np.zeros((256,1)), c='b', lw=3)
ax.set_xlim(0, 256)
ax.set_ylim(0, 5000)
plt.ion()
plt.show()

# Criação de algumas variáveis
guardaHistogramaPassado = np.zeros((256,1))
validoParaMedirADifereca = False
quantMexidas = 0

while True:
    # Capture frame por frame
    ret, frame = cap.read()

    # Se o frame estiver sido lido, ret retorna true
    if not ret:
        print("Não conseguir ler o frame do video. Webcan ainda funcioando ?")
        break
    
    # Calcula o histograma do frame
    hist = cv2.calcHist([frame],[0],None,[256], [0, 256])
    
    if validoParaMedirADifereca:
        contadorDeOcorrencias = 0
        # Verifica quantas vezes a diferença entre o novo histograma e o antigo histograma foram maiores ou igual a 70
        for i in range(256):
            calculaDiferenca = abs(int(hist[i]) - int(guardaHistogramaPassado[i]))
            if calculaDiferenca >= 70:
                contadorDeOcorrencias += 1  
        
        # Se a quantiade de ocorrências forem maiores que 200, ou seja, mais ou menos 40% das intesidades mudaram seus valores.
        # Então, quer dizer que houve uma cls
        # movimentação na cena.
        if(contadorDeOcorrencias > 200):
            quantMexidas += 1    
            print('Numero de occorências maiores que 70 >>>>', contadorDeOcorrencias)
            print('VOCÊ SE MEXEU ', quantMexidas, ' VEZES!')      
    
    # Mostra histograma no gráfico
    lineVer.set_ydata(hist)
    
    # Guarda valor do histograma
    guardaHistogramaPassado = hist
    
    # Apenas uma validação simples, para o mesmo não calcular na primeira vez que entra no while.
    validoParaMedirADifereca = True

    # Apresenta o video da camera.
    cv2.imshow('Video', frame)

    # Caso aperte q, aplicação é encerrada 
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
