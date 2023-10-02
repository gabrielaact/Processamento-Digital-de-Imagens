import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread("aurora.jpg")

if image is None:
    print("Imagem não encontrada")
else:
    # Redimensionar a imagem
    image = cv2.resize(image, (300, 300))

# Solicitar ao usuário para selecionar os pontos
p1x = int(input(f"Escolha um ponto P1(x) entre 0 e {image.shape[1]}: "))
p2x = int(input(f"Escolha um ponto P2(x) entre 0 e {image.shape[1]}: "))
p1y = int(input(f"Escolha um ponto P1(y) entre 0 e {image.shape[0]}: "))
p2y = int(input(f"Escolha um ponto P2(y) entre 0 e {image.shape[0]}: "))

# Garantir que os pontos estejam dentro dos limites da imagem
p1x = max(0, min(p1x, image.shape[1]))
p2x = max(0, min(p2x, image.shape[1]))
p1y = max(0, min(p1y, image.shape[0]))
p2y = max(0, min(p2y, image.shape[0]))

# Inverter as cores da região selecionada
for i in range(p1y, p2y):
    for j in range(p1x, p2x):
        image[i, j] = 255 - image[i, j]

# Nome do arquivo de saída
output_filename = "imagem_negativa.jpg"

# Salvar a imagem resultante
cv2.imwrite(output_filename, image)

print(f"Imagem salva como {output_filename}")

# Exibir a imagem resultante na janela
cv2.imshow("Negativo da Imagem", image)

# Aguardar até que uma tecla seja pressionada
cv2.waitKey(0)
cv2.destroyAllWindows()

