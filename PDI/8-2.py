import cv2
import numpy as np

l1 = -100
l2 = 50
d = 6
centro = 100

matriz_media_tam = 7

slider_altura = 0
slider_altura_max = 100

slider_decaimento = 0
slider_decaimento_max = 100

slider_deslocamento = 0
slider_deslocamento_max = 100

altura = 0
largura = 0

ponderada = None
ponderada_negativa = None

cap = cv2.VideoCapture(0)  # Capturar vídeo da câmera (0 para a câmera padrão)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

cv2.namedWindow("tiltshift")

def aplicar_Efeito(frame):
    global l1, l2, d, centro, altura, largura, ponderada, ponderada_negativa

    altura, largura, _ = frame.shape
    centro = slider_deslocamento * altura // 100

    for i in range(altura):
        fx = 0.0
        if d != 0:
            fx = -0.5 * (np.tanh((i - centro + l1) / d) - np.tanh((i - centro + l2) / d))
        else:
            fx = -0.5 * (np.tanh((i - centro + l1) / 0.01) - np.tanh((i - centro + l2) / 0.01))

        for j in range(largura):
            ponderada[i, j] = [fx, fx, fx]
            ponderada_negativa[i, j] = [1.0 - fx, 1.0 - fx, 1.0 - fx]

    res1 = frame * ponderada
    res2 = frame * ponderada_negativa

    resultado = cv2.addWeighted(res1, 1, res2, 1, 0)
    resultado = resultado.astype(np.uint8)

    cv2.imshow("tiltshift", resultado)

def on_trackbar_deslocamento(val):
    global slider_deslocamento, centro
    slider_deslocamento = val
    centro = slider_deslocamento * altura // 100

def on_trackbar_altura(val):
    global slider_altura, l1, l2
    slider_altura = val
    alt = altura * slider_altura // 100
    l1 = -alt // 2
    l2 = alt // 2

def on_trackbar_decaimento(val):
    global slider_decaimento, d
    slider_decaimento = val
    d = slider_decaimento

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if altura == 0:
        altura, largura, _ = frame.shape
        ponderada = np.zeros((altura, largura, 3), dtype=np.float32)
        ponderada_negativa = np.zeros((altura, largura, 3), dtype=np.float32)

        cv2.createTrackbar("Altura x {}".format(slider_altura_max), "tiltshift", slider_altura, slider_altura_max, on_trackbar_altura)
        cv2.createTrackbar("Decaimento x {}".format(slider_decaimento_max), "tiltshift", slider_decaimento, slider_decaimento_max, on_trackbar_decaimento)
        cv2.createTrackbar("Deslocamento x {}".format(slider_deslocamento_max), "tiltshift", slider_deslocamento, slider_deslocamento_max, on_trackbar_deslocamento)

    on_trackbar_altura(slider_altura)
    on_trackbar_decaimento(slider_decaimento)
    on_trackbar_deslocamento(slider_deslocamento)

    aplicar_Efeito(frame)

    key = cv2.waitKey(1)
    if key == 27:  # Pressione a tecla Esc para sair
        break

cap.release()
cv2.destroyAllWindows()

