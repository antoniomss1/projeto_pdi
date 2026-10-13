"""Aguçamento: Laplaciano e high boost."""
import numpy as np
from . import convolucao as conv


def agucar_laplaciano(img, c=1.0, variante="4-vizinhos", borda="replicar"):
    """TODO: g = f + c * lap(f).
    O sinal de c depende do sinal do centro da máscara (centro negativo -> subtrair)."""
    if (variante == "4-vizinhos"):
        w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    else:
        w = np.array([[ 1,  1,  1],
                    [ 1, -8,  1],
                    [ 1,  1,  1]])
    # 1. Pega os gradientes BRUTOS (com valores negativos intactos)

    laplaciano = conv.convolver(img, w, offset=0, borda=borda, faixa="bruto")

    g = img.astype(np.float64) - c * laplaciano

    return np.clip(g, 0, 255).astype(np.uint8)

def high_boost(img, A=1.5, n=3, borda="replicar"):
    kernel_media = np.ones((n, n), dtype=np.float64) / (n * n)
    
    suavizada = conv.convolver(img, kernel_media, offset=0, borda=borda, faixa="bruto")
    
    img_float = img.astype(np.float64)
    g = (A * img_float) - suavizada
    
    return np.clip(g, 0, 255).astype(np.uint8)
