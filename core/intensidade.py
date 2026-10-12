"""Operações algébricas e transformações de intensidade (IMPLEMENTADAS no protótipo).

Todas recebem/devolvem matrizes 2D uint8. Cálculos internos em float64
para evitar overflow de uint8.
"""
import numpy as np
from . import utils


def negativo(img):
    """s = 255 - r"""
    return (255 - img.astype(np.int32)).astype(np.uint8)
    #return (255 - img.astype(np.int32)).astype(np.uint8)


def limiarizacao(img, T=128):
    """s = 255 se r >= T, senão 0"""
    #return (img >= T ? 255 : 0)
    return np.where(img >= T, 255, 0).astype(np.uint8)


def alargamento_contraste(img, r1, s1, r2, s2):
    """Função linear por partes definida por (r1,s1) e (r2,s2). Usa tabela (LUT)."""
    rmax = np.max(img)
    rmin = np.min(img)

    nimg = ((s2 - s1)/(rmax - rmin))*(img-rmin)+s1
    return nimg.astype(np.uint8)

#    lut = np.zeros(256)
#    for r in range(256):
#        if r < r1:
#            lut[r] = s1 * r / r1 if r1 > 0 else s1
#        elif r <= r2:
#            lut[r] = s1 + (s2 - s1) * (r - r1) / (r2 - r1) if r2 > r1 else s1
#        else:
#            lut[r] = s2 + (255 - s2) * (r - r2) / (255 - r2) if r2 < 255 else s2
#    return utils.ajustar_faixa(lut[img], "clamp")


def gamma(img, c=1.0, gamma=1.0):
    """s = c * 255 * (r/255)^gamma"""
    nimg = ((img.astype(np.float64)/255.0) ** (gamma)) * c * 255.0
    #s = c * 255.0 * (img.astype(np.float64) / 255.0) ** gamma
    #return utils.ajustar_faixa(s, "clamp")
    return utils.ajustar_faixa(nimg, "clamp")


def logaritmo(img, c=46.0):
    """s = c * ln(1 + r).  c ~ 255/ln(256) = 46.0 mapeia 255 -> 255."""
    nimg = c * np.log(1 + img.astype(np.float64))
    #s = c * np.log1p(img.astype(np.float64))
    return utils.ajustar_faixa(nimg, "clamp")


def dissolve_uniforme(img_a, img_b, alpha=0.5):
    """g = t*A + (1-alpha)*B, alpha constante."""
    t = alpha
    nimg = (1-t)*img_a.astype(np.float64) + (t) * img_b.astype(np.float64)

    #g = t * img_a.astype(np.float64) + (1 - alpha) * img_b.astype(np.float64)
    return utils.ajustar_faixa(nimg, "clamp")


def dissolve_nao_uniforme(img_a, img_t, img_b):
    """alpha varia linearmente da coluna 0 até a última coluna.
    (Confira na disciplina se o 'não uniforme' do enunciado segue outra regra.)"""
    nimg = (1-img_t.astype(np.float64)/255)*img_a + (img_t.astype(np.float64)/255)*img_b
    return utils.ajustar_faixa(nimg, "clamp")

#    larg = img_a.shape[1]
#    alpha = np.linspace(alpha_ini, alpha_fim, larg)[np.newaxis, :]
#    g = alpha * img_a.astype(np.float64) + (1 - alpha) * img_b.astype(np.float64)
#    return utils.ajustar_faixa(g, "clamp")
