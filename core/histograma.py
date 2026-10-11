"""Histograma, expansão e equalização."""
import numpy as np


def calcular_histograma(img) -> np.ndarray:
    """Vetor de 256 posições com a contagem de pixels de cada nível. (IMPLEMENTADO)"""
    h = np.zeros(256, dtype=np.int64)
    for linha in img:
        for v in linha:
            h[v] += 1
    return h


def expandir(img):
    """TODO: expansão (alargamento linear) de [min, max] da imagem para [0, 255].
    s = (r - min) * 255 / (max - min).  Cuidado com max == min."""
    raise NotImplementedError("histograma.expandir")


def equalizar(img):
    """TODO: equalização.
    1) h = histograma  2) p = h / total  3) cdf = soma acumulada de p
    4) s = round(255 * cdf[r])  5) aplicar a tabela (LUT) em cada pixel."""
    raise NotImplementedError("histograma.equalizar")
