"""Detecção de bordas: Roberts, Sobel, Kirsch e Laplaciano.
Todos podem reaproveitar convolucao.convolver (versão bruta, em float)."""


def roberts(img, metodo="raiz", borda="replicar", faixa="normalizar"):
    """TODO: duas máscaras 2x2. metodo: 'raiz' -> sqrt(Gx²+Gy²) | 'soma_abs' -> |Gx|+|Gy|."""
    raise NotImplementedError("bordas.roberts")


def sobel(img, metodo="raiz", borda="replicar", faixa="normalizar"):
    """TODO: Gx e Gy 3x3. Mostre também Gx e Gy separadamente no relatório."""
    raise NotImplementedError("bordas.sobel")


def kirsch(img, borda="replicar", faixa="normalizar"):
    """TODO: 8 máscaras direcionais 3x3; resposta final = máximo das 8 respostas por pixel."""
    raise NotImplementedError("bordas.kirsch")


def laplaciano(img, variante="4-vizinhos", borda="replicar", faixa="normalizar"):
    """TODO: máscara 4-vizinhos ou 8-vizinhos. Resposta tem valores negativos: trate a faixa."""
    raise NotImplementedError("bordas.laplaciano")
