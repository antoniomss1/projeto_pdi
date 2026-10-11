"""Filtros de vizinhança: média e mediana."""


def media(img, n=3, borda="replicar"):
    """TODO: para cada pixel, média da janela n x n.
    Dica: use utils.preencher_borda(img, n//2, n//2, n//2, n//2, borda)."""
    raise NotImplementedError("vizinhanca.media")


def mediana(img, n=3, borda="replicar"):
    """TODO: para cada pixel, mediana (ordenar e pegar o valor central) da janela n x n.
    É um filtro NÃO linear: não dá para fazer por convolução."""
    raise NotImplementedError("vizinhanca.mediana")
