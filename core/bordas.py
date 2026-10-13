"""Detecção de bordas: Roberts, Sobel, Kirsch e Laplaciano.
Todos podem reaproveitar convolucao.convolver (versão bruta, em float)."""

from . import convolucao as conv
import numpy as np
from . import utils # Para usar o ajustar_faixa no final

def roberts(img, metodo="raiz", borda="replicar", faixa="normalizar"):
    """
    Filtro de bordas de Roberts Cross (máscaras cruzadas 2x2).
    """
    wx = np.array([[-1, 0], 
                   [ 0, 1]])
                   
    wy = np.array([[ 0, -1], 
                   [ 1,  0]])

    # 1. Pega os gradientes BRUTOS (com valores negativos intactos)
    gx = conv.convolver(img, wx, offset=0, borda=borda, faixa="bruto")
    gy = conv.convolver(img, wy, offset=0, borda=borda, faixa="bruto")

    # 2. Combina as energias dos dois eixos
    if metodo == "raiz":
        # np.square é um pouco mais rápido/limpo que (gx)*(gx), mas ambos funcionam!
        nimg = np.sqrt(np.square(gx) + np.square(gy))
    else:
        nimg = np.absolute(gx) + np.absolute(gy)

    # 3. Agora sim, com a imagem final montada, ajustamos a faixa e cortamos
    nimg_ajustada = utils.ajustar_faixa(nimg, faixa)
    
    return nimg_ajustada.astype(np.uint8)

def sobel(img, metodo="raiz", borda="replicar", faixa="normalizar"):
    """TODO: Gx e Gy 3x3. Mostre também Gx e Gy separadamente no relatório."""
    wx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
                   
    wy = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2,-1]])

    # 1. Pega os gradientes BRUTOS (com valores negativos intactos)
    gx = conv.convolver(img, wx, offset=0, borda=borda, faixa="bruto")
    gy = conv.convolver(img, wy, offset=0, borda=borda, faixa="bruto")

    # 2. Combina as energias dos dois eixos
    if metodo == "raiz":
        # np.square é um pouco mais rápido/limpo que (gx)*(gx), mas ambos funcionam!
        nimg = np.sqrt(np.square(gx) + np.square(gy))
    else:
        nimg = np.absolute(gx) + np.absolute(gy)

    # 3. Agora sim, com a imagem final montada, ajustamos a faixa e cortamos
    nimg_ajustada = utils.ajustar_faixa(nimg, faixa)
    return nimg_ajustada.astype(np.uint8)


def kirsch(img, borda="replicar", faixa="normalizar"):
    """Filtro de Kirsch: Aplica 8 máscaras direcionais 3x3 e retém o valor máximo por pixel."""
    
    mascaras = [
        np.array([[ 5,  5,  5], [-3,  0, -3], [-3, -3, -3]]),
        np.array([[ 5,  5, -3], [ 5,  0, -3], [-3, -3, -3]]),
        np.array([[ 5, -3, -3], [ 5,  0, -3], [ 5, -3, -3]]),
        np.array([[-3, -3, -3], [ 5,  0, -3], [ 5,  5, -3]]),
        np.array([[-3, -3, -3], [-3,  0, -3], [ 5,  5,  5]]),
        np.array([[-3, -3, -3], [-3,  0,  5], [-3,  5,  5]]),
        np.array([[-3, -3,  5], [-3,  0,  5], [-3, -3,  5]]),
        np.array([[-3,  5,  5], [-3,  0,  5], [-3, -3, -3]]) 
    ]

    nimg = np.zeros_like(img, dtype=float)

    for w in mascaras:
        g = conv.convolver(img, w, offset=0, borda=borda, faixa="bruto")
        nimg = np.maximum(nimg, g)

    nimg_ajustada = utils.ajustar_faixa(nimg, faixa)
    return nimg_ajustada.astype(np.uint8)


def laplaciano(img, variante="4-vizinhos", borda="replicar", faixa="normalizar"):
    """TODO: máscara 4-vizinhos ou 8-vizinhos. Resposta tem valores negativos: trate a faixa."""
    if (variante == "4-vizinhos"):
        w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    else:
        w = np.array([[ 1,  1,  1],
                    [ 1, -8,  1],
                    [ 1,  1,  1]])
    # 1. Pega os gradientes BRUTOS (com valores negativos intactos)
    g = conv.convolver(img, w, offset=0, borda=borda, faixa="bruto")

    # 3. Agora sim, com a imagem final montada, ajustamos a faixa e cortamos
    nimg_ajustada = np.absolute(g)
    return nimg_ajustada.astype(np.uint8)

