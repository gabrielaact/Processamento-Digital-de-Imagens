import cv2
import numpy as np

# Definição do número de clusters desejados e o número de rodadas do algoritmo k-means
n_clusters = 6
n_rodadas = 1

# Carregar a imagem
img = cv2.imread("aurora.jpg")

if (img is None):
    sys.exit("Imagem não encontrada.")

# Reformatação da matriz de pixels para preparar os dados para o k-means
samples = img.reshape((-1, 3))
samples = np.float32(samples)

# Definição dos critérios de parada para o algoritmo k-means
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)

# Aplicação do algoritmo k-means aos dados de amostra
_, labels, centers = cv2.kmeans(samples, n_clusters, None, criteria, n_rodadas, cv2.KMEANS_RANDOM_CENTERS)

# Conversão dos centros dos clusters para o tipo de dados uint8
centers = np.uint8(centers)

# Criar imagem segmentada, onde cada pixel é substituído pelo valor do centroide do cluster
segmented_image = centers[labels.flatten()]
segmented_image = segmented_image.reshape(img.shape)

# Exibir da imagem segmentada 
cv2.imshow("clustered image", segmented_image)

# Salvar imagem segmentada
cv2.imwrite("aurora_clustered.jpg", segmented_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

