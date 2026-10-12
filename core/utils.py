"""Funções auxiliares: E/S de imagem, ajuste de faixa e preenchimento de bordas.

Bibliotecas (Pillow/NumPy) são usadas aqui apenas como infraestrutura:
ler/salvar arquivos, guardar a imagem em matriz e preencher bordas.
As operações de processamento em si ficam nos demais módulos.
"""
import numpy as np
from PIL import Image

MODOS_BORDA = ["zeros", "replicar", "espelhar"]
MODOS_FAIXA = ["clamp", "normalizar", "modulo"]


# ----------------------------------------------------------------- E/S
def carregar_cinza(arquivo) -> np.ndarray:
    """Lê uma imagem e devolve matriz 2D uint8 em escala de cinza."""
    return np.array(Image.open(arquivo).convert("L"), dtype=np.uint8)


def carregar_cinza_redimensionada(arquivo, shape) -> np.ndarray:
    """Lê uma imagem e a redimensiona para (altura, largura) = shape."""
    img = Image.open(arquivo).convert("L").resize((shape[1], shape[0]))
    return np.array(img, dtype=np.uint8)


def para_pil(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.asarray(arr).astype(np.uint8))


def imagem_exemplo(tam: int = 256) -> np.ndarray:
    """Imagem sintética (gradiente + formas + ruído) para testar sem upload."""
    y, x = np.mgrid[0:tam, 0:tam]
    img = 40 + 120 * (x / (tam - 1))
    cx = cy = tam // 2
    img[(x - cx) ** 2 + (y - cy) ** 2 < (tam // 4) ** 2] = 200
    img[tam // 8: tam // 8 + tam // 6, tam // 8: tam // 8 + tam // 3] = 90
    img = img + np.random.default_rng(0).normal(0, 8, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


# ------------------------------------------------------- faixa [0, 255]
def clamp(a: np.ndarray):
    return np.clip(a, 0, 255)


def normalizar(a: np.ndarray):
    """Reescala linearmente [min, max] -> [0, 255]."""
    a = a.astype(np.float64)
    mn, mx = a.min(), a.max()
    if mx == mn:
        return np.zeros(a.shape)
    return (a - mn) * 255.0 / (mx - mn)


def ajustar_faixa(a: np.ndarray, modo: str = "clamp"):
    """Converte resultado (float/int, possivelmente fora de [0,255]) em uint8.

    clamp      : corta valores < 0 em 0 e > 255 em 255
    normalizar : reescala min-max para [0, 255]
    modulo     : |valor| e depois clamp
    """
    if modo == "clamp":
        r = clamp(a)
    elif modo == "normalizar":
        r = normalizar(a)
    elif modo == "modulo":
        r = clamp(np.abs(a))
    else:
        raise ValueError(f"Modo de faixa desconhecido: {modo}")
    return np.rint(r).astype(np.uint8)


# ----------------------------------------------------------------- bordas
def preencher_borda(img, topo, baixo, esq, dir_, modo="replicar"):
    """Acrescenta margens à imagem para que máscaras/janelas caibam nas bordas."""
    tipo = {"zeros": "constant", "replicar": "edge", "espelhar": "reflect"}[modo]
    return np.pad(img, ((topo, baixo), (esq, dir_)), mode=tipo)
