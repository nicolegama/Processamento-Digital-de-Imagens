#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

NEGATIVO = False
THRESHOLD = 0.78
ALTURA_MIN = 1
LARGURA_MIN = 1
N_PIXELS_MIN = 20

#===============================================================================

def binariza (img, threshold):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x, 0] > threshold:
                img[y, x, 0] = 1
            else:
                img[y, x, 0] = 0
    return img
#0 fundo 1 arroz

''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

#-------------------------------------------------------------------------------

def rotula (img, largura_min, altura_min, n_pixels_min):
    componentes = []
    rotulo = 2  # começa em 2

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x, 0] == 1.0:
                #cria o dicionario p armazenar os dados do componente
                comp = {
                    'label': rotulo,
                    'n_pixels': 0,
                    'T': y,
                    'B': y,
                    'L': x,
                    'R': x,
                }

                flood_fill(img, y, x, rotulo, comp)

                # calcula dimensões da caixa
                largura_comp = comp['R'] - comp['L'] + 1
                altura_comp  = comp['B'] - comp['T'] + 1
                
                # descarta componentes pequenas demais
                if (largura_comp >= largura_min and
                    altura_comp  >= altura_min  and
                    comp['n_pixels'] >= n_pixels_min):
                    componentes.append(comp)

                rotulo += 1

    return componentes

'''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

#-------------------------------------------------------------------------------
    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

def flood_fill(img, y, x, rotulo, componente):
    altura, largura = img.shape[0], img.shape[1]

    #checa os limites da img
    if y < 0 or y >= altura: return
    if x < 0 or x >= largura: return

    if img[y, x, 0] != 1.0: return

    img[y, x, 0] = rotulo

    #atualiza os dados do componente
    componente['n_pixels'] += 1

    if y < componente['T']: componente['T'] = y
    if y > componente['B']: componente['B'] = y
    if x < componente['L']: componente['L'] = x
    if x > componente['R']: componente['R'] = x

    flood_fill(img, y-1, x, rotulo, componente)
    flood_fill(img, y+1, x, rotulo, componente)
    flood_fill(img, y, x-1, rotulo, componente)
    flood_fill(img, y, x+1, rotulo, componente)

#===============================================================================

def main ():
    # Abre a imagem em escala de CINZA.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape[0], img.shape[1], 1))
    img = img.astype (np.float32) / 255 #NORMALIZA A IMAGEM

    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    if NEGATIVO:
        img = 1 - img

    img = binariza (img, THRESHOLD)

    cv2.imshow ('01 - binarizada', img)
    cv2.waitKey(0)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)

    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    for c in componentes:
        cv2.rectangle (img_out, (c['L'], c['T']), (c['R'], c['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

#===============================================================================

if __name__ == '__main__':
    main ()
