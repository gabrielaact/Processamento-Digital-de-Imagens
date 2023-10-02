import cv2

# Carregar a imagem
imagemFinal = cv2.imread("esteganografia.png")

# Verificar se a imagem foi carregada com sucesso
if imagemFinal is None:
    print("Imagem não encontrada")
else:
    # Clonar a imagem para trabalhar com uma cópia
    imagemEscondida = imagemFinal.copy()

    # Exibir a imagem original
    cv2.imshow("", imagemFinal)
    cv2.waitKey()
    cv2.destroyWindow("")

    nbits = 3  # Número de bits para deslocamento

    # Aplicar o deslocamento nos canais de cores
    for i in range(imagemEscondida.shape[0]):
        for j in range(imagemEscondida.shape[1]):
            valEscondida = imagemEscondida[i, j]
            valEscondida[0] = valEscondida[0] << (8 - nbits)
            valEscondida[1] = valEscondida[1] << (8 - nbits)
            valEscondida[2] = valEscondida[2] << (8 - nbits)
            imagemEscondida[i, j] = valEscondida

    # Exibir a imagem com os canais deslocados
    cv2.imshow("", imagemEscondida)
    # Nome do arquivo de saída
    output_filename = "esteganografia_escondida.jpg"

    # Salvar a imagem resultante
    cv2.imwrite(output_filename, imagemEscondida)
    cv2.waitKey()
    cv2.destroyAllWindows()
