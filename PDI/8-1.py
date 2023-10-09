import cv2
import numpy as np

# Parâmetros iniciais
l1 = -100
l2 = 50
d = 6
centro = 100
matriz_media_tam = 7
altura = 0
largura = 0
slider_altura = 0
slider_altura_max = 100
slider_decaimento = 0
slider_decaimento_max = 100
slider_deslocamento = 0
slider_deslocamento_max = 100
imagem = None
imagem_borrada = None
ponderada = None
ponderada_negativa = None

def addEffect():
    global l1, l2, d, centro, altura, largura, imagem, imagem_borrada, ponderada, ponderada_negativa

    altura, largura, _ = imagem.shape
    centro = slider_deslocamento * altura // 100

    # Calcular a ponderação para o efeito tilt-shift
    for i in range(altura):
        fx = 0.0
        if d != 0:
            fx = -0.5 * (np.tanh((i - centro + l1) / d) - np.tanh((i - centro + l2) / d))
        else:
            fx = -0.5 * (np.tanh((i - centro + l1) / 0.01) - np.tanh((i - centro + l2) / 0.01))

        for j in range(largura):
            ponderada[i, j] = [fx, fx, fx]
            ponderada_negativa[i, j] = [1.0 - fx, 1.0 - fx, 1.0 - fx]

    # Aplicar o efeito ponderado na imagem original e na imagem borrada
    res1 = imagem * ponderada
    res2 = imagem_borrada * ponderada_negativa

    # Combinar as duas imagens resultantes
    resultado = cv2.addWeighted(res1, 1, res2, 1, 0)
    resultado = resultado.astype(np.uint8)

    # Exibir o resultado
    cv2.imshow("tiltshift", resultado)

# Funções para atualizar os parâmetros via trackbars
def on_trackbar_deslocamento(val):
    global slider_deslocamento, centro
    slider_deslocamento = val
    centro = slider_deslocamento * altura // 100
    addEffect()

def on_trackbar_altura(val):
    global slider_altura, l1, l2
    slider_altura = val
    alt = altura * slider_altura // 100
    l1 = -alt // 2
    l2 = alt // 2
    addEffect()

def on_trackbar_decaimento(val):
    global slider_decaimento, d
    slider_decaimento = val
    d = slider_decaimento
    addEffect()

if __name__ == "__main__":
    # Criar uma matriz de filtro de média para borrar a imagem
    media = np.full((matriz_media_tam, matriz_media_tam), 1.0 / (matriz_media_tam * matriz_media_tam), dtype=np.float32)
    masc_media = np.float32(media)

    # Carregar a imagem e aplica um filtro de média
    imagem = cv2.imread("aurora.jpg").astype(np.float32)
    imagem_borrada = cv2.filter2D(imagem, -1, masc_media)

    largura = imagem.shape[1]
    altura = imagem.shape[0]

    ponderada = np.zeros((altura, largura, 3), dtype=np.float32)
    ponderada_negativa = np.zeros((altura, largura, 3), dtype=np.float32)

    # Criar uma janela para exibir o resultado
    cv2.namedWindow("tiltshift", cv2.WINDOW_NORMAL)

    # Criar trackbars para controlar os parâmetros
    cv2.createTrackbar("Altura x {}".format(slider_altura_max), "tiltshift", slider_altura, slider_altura_max, on_trackbar_altura)
    on_trackbar_altura(slider_altura)

    cv2.createTrackbar("Decaimento x {}".format(slider_decaimento_max), "tiltshift", slider_decaimento, slider_decaimento_max, on_trackbar_decaimento)
    on_trackbar_decaimento(slider_decaimento)

    cv2.createTrackbar("Deslocamento x {}".format(slider_deslocamento_max), "tiltshift", slider_deslocamento, slider_deslocamento_max, on_trackbar_deslocamento)
    on_trackbar_deslocamento(slider_deslocamento)

    addEffect()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

