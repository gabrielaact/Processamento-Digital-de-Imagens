import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Deu ruim")
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("largura =", width)
    print("altura =", height)

    nbins = 64
    histw = nbins
    histh = nbins // 2

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Dividir os canais de cores
        b, g, r = cv2.split(frame)

        # Equalizar o histograma dos canais de cores
        b_eq = cv2.equalizeHist(b)
        g_eq = cv2.equalizeHist(g)
        r_eq = cv2.equalizeHist(r)

        # Mesclar os canais de volta para formar a imagem colorida equalizada
        equalized_frame = cv2.merge([b_eq, g_eq, r_eq])

        # Calcular e exibir os histogramas
        hist_b = cv2.calcHist([b], [0], None, [nbins], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [nbins], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [nbins], [0, 256])

        hist_b = cv2.normalize(hist_b, hist_b, 0, histh, cv2.NORM_MINMAX)
        hist_g = cv2.normalize(hist_g, hist_g, 0, histh, cv2.NORM_MINMAX)
        hist_r = cv2.normalize(hist_r, hist_r, 0, histh, cv2.NORM_MINMAX)

        hist_b = hist_b.astype(np.uint8)
        hist_g = hist_g.astype(np.uint8)
        hist_r = hist_r.astype(np.uint8)

        hist_img_b = np.zeros((histh, histw, 3), dtype=np.uint8)
        hist_img_g = np.zeros((histh, histw, 3), dtype=np.uint8)
        hist_img_r = np.zeros((histh, histw, 3), dtype=np.uint8)

        for i in range(1, nbins):
            cv2.line(hist_img_b, (i - 1, histh - int(hist_b[i - 1][0])), (i, histh - int(hist_b[i][0])), (255, 0, 0), 1)
            cv2.line(hist_img_g, (i - 1, histh - int(hist_g[i - 1][0])), (i, histh - int(hist_g[i][0])), (0, 255, 0), 1)
            cv2.line(hist_img_r, (i - 1, histh - int(hist_r[i - 1][0])), (i, histh - int(hist_r[i][0])), (0, 0, 255), 1)

        cv2.imshow("Resultado", equalized_frame)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

