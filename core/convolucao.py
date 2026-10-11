"""Convolução genérica: g = f * h + offset.  (NÚCLEO DO PROJETO)"""


def convolver(img, mascara, offset=0, borda="replicar", faixa="clamp"):
    """TODO.
    img     : matriz 2D uint8
    mascara : matriz n x m (float) -- n e m podem ser diferentes
    offset  : constante somada ao resultado (ex.: 128 no relevo)
    borda   : 'zeros' | 'replicar' | 'espelhar'
    faixa   : 'clamp' | 'normalizar' | 'modulo'  (-> utils.ajustar_faixa)

    Passos: preencher borda -> para cada pixel somar mascara*vizinhança (em float!)
    -> somar offset -> ajustar faixa -> uint8.
    Atenção: convolução INVERTE a máscara (rotaciona 180°); correlação não.
    Decida qual usar e documente no relatório.
    Também exponha uma versão que devolve o resultado BRUTO (float, sem ajuste de faixa):
    Sobel, Kirsch, Roberts e Laplaciano precisam dele para combinar respostas."""
    raise NotImplementedError("convolucao.convolver")
