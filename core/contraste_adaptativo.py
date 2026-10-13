"""Controle de contraste adaptativo (média e desvio padrão locais)."""
import numpy as np

def contraste_adaptativo(img, c=1.0, n=3, borda="replicar"):
    l, cols = img.shape
    f = img.astype(np.float64)
    
    p = n // 2
    modo_pad = "constant" if borda == "zero" else "edge"
    bdd = np.pad(f, p, mode=modo_pad)
    
    pilha = np.zeros((n * n, l, cols), dtype=np.float64)
    camada = 0
    for u in range(n):
        for v in range(n):
            pilha[camada] = bdd[u:u+l, v:v+cols]
            camada += 1
 
    mu = np.mean(pilha, axis=0)
    sigma = np.std(pilha, axis=0)

    g = np.copy(f)
 
    masc = sigma != 0

    g[masc] = mu[masc] + (c / sigma[masc]) * (f[masc] - mu[masc])
 
    return np.clip(g, 0, 255).astype(np.uint8)

