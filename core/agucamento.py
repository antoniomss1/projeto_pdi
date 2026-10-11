"""Aguçamento: Laplaciano e high boost."""


def agucar_laplaciano(img, c=1.0, variante="4-vizinhos", borda="replicar"):
    """TODO: g = f + c * lap(f).
    O sinal de c depende do sinal do centro da máscara (centro negativo -> subtrair)."""
    raise NotImplementedError("agucamento.agucar_laplaciano")


def high_boost(img, A=1.5, n=3, borda="replicar"):
    """TODO: g = A*f - suavizada(f)  (equivale a f + (A-1)*f + (f - suavizada)... confira a forma da aula)."""
    raise NotImplementedError("agucamento.high_boost")
