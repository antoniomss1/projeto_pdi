"""Convolução genérica: g = f * h + offset.  (NÚCLEO DO PROJETO)"""
import numpy as np
from . import utils as ut


def convolver(img, mascara, offset=0, borda="replicar", faixa="clamp"):
    kernel = mascara
    H, W = img.shape
    m, n = kernel.shape
    
    a = m // 2
    b = n // 2
    
    w_invertido = np.flip(kernel)
    
    dicionario_borda = {"zeros": "constant", "replicar": "edge", "espelhar": "reflect"}
    modo_pad = dicionario_borda.get(borda, "edge") 
    
    bdd = np.pad(img.astype(np.float64), ((a, a), (b, b)), mode=modo_pad)
    
    resultado = np.zeros((H, W), dtype=np.float64)
    
    for s in range(m):
        for t in range(n):
            peso = w_invertido[s, t]
            if peso != 0:
                resultado += peso * bdd[s:s+H, t:t+W]
                
    
    resultado += offset
    
    if faixa == "bruto" or faixa is None:
        return resultado
        
    resultado_ajustado = ut.ajustar_faixa(resultado, faixa)
    
    return resultado_ajustado
