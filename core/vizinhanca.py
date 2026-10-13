"""Filtros de vizinhança: média e mediana."""
import numpy as np
from . import utils as ut


def media(img, n=3, borda="replicar"):
    """TODO: para cada pixel, média da janela n x n.
    Dica: use utils.preencher_borda(img, n//2, n//2, n//2, n//2, borda)."""
    l,c = img.shape
    p = n//2
    #bdd = np.pad(img.astype(np.float64), p, mode="edge")
    bdd = ut.preencher_borda(img, n//2, n//2, n//2, n//2, borda)
    nimg = np.zeros((l, c))
    for u in range(n):
        for v in range(n):
            nimg += bdd[u:u+l,v:v+c]
    average = nimg / (n*n)

    return average.astype(np.uint8)
    #raise NotImplementedError("vizinhanca.media")


def mediana(img, n=3, borda="replicar"):
    """TODO: para cada pixel, mediana (ordenar e pegar o valor central) da janela n x n.
    É um filtro NÃO linear: não dá para fazer por convolução."""

    l,c = img.shape
    p = n//2
    #bdd = np.pad(img.astype(np.float64), p, mode="edge")
    bdd = ut.preencher_borda(img, n//2, n//2, n//2, n//2, borda)
    nimg = np.zeros((l, c))

    pilha = np.zeros((n * n, l, c), dtype=img.dtype)
    camada = 0 
    for u in range(n):
        for v in range(n):
            pilha[camada] = bdd[u:u+l, v:v+c]
            camada += 1
    
    nimg = np.median(pilha, axis=0)
    
    return nimg.astype(np.uint8)

    #raise NotImplementedError("vizinhanca.mediana")
