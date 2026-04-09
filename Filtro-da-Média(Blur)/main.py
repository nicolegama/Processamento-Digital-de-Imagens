import sys
import timeit
import numpy as np
import cv2
import time

INPUT_IMAGE= 'cachorro-bobo.jpeg'
JANELA = 10

def media_ingenuo(img, JANELA, saida):

    h, w, c = img.shape #altura, largura, canais

    for y in range(h):
        for x in range(w):
            for canal in range(c):
                soma = 0
                count = 0

                #janela adaptativa
                for i in range(max(0, y - JANELA//2), min(h, y + JANELA//2 + 1)):
                    for j in range(max(0, x - JANELA//2), min(w, x + JANELA//2 + 1)):
                        soma += img[i][j][canal]
                        count += 1

                saida[y][x][canal] = soma / count

#===============================================================================
def media_separavel(img, JANELA, saida):
    #precisa de buffer auxiliar
    h, w, c = img.shape

    temp = img.copy()

    # horizontal
    for y in range(h):
        for x in range(w):
            for canal in range(c):
                soma = 0
                count = 0

                for j in range(max(0, x - JANELA//2), min(w, x + JANELA//2 + 1)):
                    soma += img[y][j][canal]
                    count += 1

                temp[y][x][canal] = soma / count

    # vertical 
    for y in range(h):
        for x in range(w):
            for canal in range(c):
                soma = 0
                count = 0

                for i in range(max(0, y - JANELA//2), min(h, y + JANELA//2 + 1)):
                    soma += temp[i][x][canal]
                    count += 1

                saida[y][x][canal] = soma / count

#===============================================================================
def media_integral(img, JANELA, saida):
    #precisa de buffer auxiliar
    integral = np.zeros_like(img) #matriz pras somas
    h, w, c = img.shape

    #integral
    for y in range(h):
        for x in range(w):
            for canal in range(c):
                integral[y][x][canal] = img[y][x][canal]
                if y > 0: #trata as bordas
                    integral[y][x][canal] += integral[y-1][x][canal]
                if x > 0:
                    integral[y][x][canal] += integral[y][x-1][canal]
                if y > 0 and x > 0:
                    integral[y][x][canal] -= integral[y-1][x-1][canal]
                        
    #calcula o blur
    for y in range(h):
        for x in range(w):
            for canal in range(c):
                #tamanho janela
                y1 = max(0, y - JANELA//2)
                y2 = min(h-1, y + JANELA//2)
                x1 = max(0, x - JANELA//2)
                x2 = min(w-1, x + JANELA//2)

                soma = integral[y2][x2][canal]

                if y1 > 0:
                    soma -= integral[y1-1][x2][canal]
                if x1 > 0:
                    soma -= integral[y2][x1-1][canal]
                if y1 > 0 and x1 > 0:
                    soma += integral[y1-1][x1-1][canal]
                area = (y2 - y1 + 1) * (x2 - x1 + 1)

                saida[y][x][canal] = soma / area

#===============================================================================
def main():
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()


    img = img.astype (np.float32) / 255 #NORMALIZA A IMAGEM

    saida = img.copy()

    print( "Tamanho da janela:", JANELA)

    print("\n##Algoritmo ingênuo##")
    start_time = time.perf_counter()
    media_ingenuo(img, JANELA, saida)
    end_time = time.perf_counter()

    print("Tempo de execução:", end_time - start_time ,"segundos")

    cv2.imshow ('01 - original', img)

    cv2.imshow ('01 - borrada ingenuo', saida)

    print("\n##Algoritmo menos ingênuo: separável##")
    start_time = time.perf_counter()
    media_separavel(img, JANELA, saida)
    end_time = time.perf_counter()
    print("Tempo de execução:", end_time - start_time , "segundos")

    cv2.imshow ('01 - borrada separavel', saida)

    print("\n##Algoritmo com imagens integrais#")
    start_time = time.perf_counter()
    media_integral(img, JANELA, saida)
    end_time = time.perf_counter()
    print("Tempo de execução:", end_time - start_time , "segundos")

    cv2.imshow ('01 - borrada integral', saida)

    print("\n##Algoritmo OpenCV#")
    start_time = time.perf_counter()
    blur = cv2.blur(img, (JANELA, JANELA))
    end_time = time.perf_counter()
    print("Tempo de execução:", end_time - start_time , "segundos")

    cv2.imshow ('01 - borrada open cv', blur)


    cv2.waitKey ()

 #===============================================================================

if __name__ == '__main__':
    main ()
