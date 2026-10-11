# Guia para continuar o projeto — Sistema de Processamento de Imagens

## 1. Como rodar

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 2. O que já está pronto e o que falta

| Módulo | Status | Observação |
|---|---|---|
| `app.py` (interface) | Pronto | Todas as operações já têm controles e estão ligadas às funções de `core/` |
| `core/utils.py` | Pronto | E/S, ajuste de faixa, preenchimento de bordas |
| `core/intensidade.py` | Pronto | Negativo, limiar, alargamento, gamma, log, dissolve |
| `core/histograma.py` | Parcial | Só `calcular_histograma`. Faltam `expandir` e `equalizar` |
| `core/convolucao.py` | **A fazer** | Núcleo do projeto |
| `core/vizinhanca.py` | **A fazer** | Média e mediana |
| `core/bordas.py` | **A fazer** | Roberts, Sobel, Kirsch, Laplaciano |
| `core/agucamento.py` | **A fazer** | Laplaciano e high boost |
| `core/contraste_adaptativo.py` | **A fazer** | Média/desvio padrão locais |

Enquanto uma função lança `NotImplementedError`, a interface mostra um aviso 🚧 e continua funcionando.
Ao implementar, **mantenha a assinatura** da função: a interface já a chama com esses parâmetros.

> Revise o que o prototipo implementou (dissolve não uniforme, alargamento, log) contra as
> definições das **suas notas de aula**. Fórmulas "da disciplina" podem diferir um pouco.

## 3. Ordem recomendada

### Etapa 1 — Convolução (`convolucao.py`)
1. Preencha as bordas com `utils.preencher_borda` (margem de `n//2` linhas e `m//2` colunas).
2. Converta para `float64` **antes** de multiplicar (overflow em `uint8` é o bug clássico).
3. Para cada pixel `(i, j)`: some `mascara[u, v] * janela[u, v]`.
4. Some o `offset` e use `utils.ajustar_faixa(resultado, faixa)`.
5. Decida e documente: **convolução** (máscara rotacionada 180°) ou **correlação**?
6. Crie uma segunda função que devolva o resultado **bruto** (float, sem ajuste). Bordas e aguçamento precisam dela.

Teste rápido: máscara identidade (1 no centro) devolve a imagem original; máscara `ones/9` deve se comportar como a média.

### Etapa 2 — Aplicações diretas da convolução
- **Relevo e aguçamento (c, d):** são só máscaras diferentes na tela de convolução. Pegue as máscaras exatas do enunciado e salve-as como presets em `PRESETS` no `app.py`.
- **Sobel:** `Gx`, `Gy` + magnitude. Mostre `Gx` e `Gy` separados no relatório.
- **Roberts:** duas máscaras 2x2 (cuidado: máscara par, centro não é único; defina o posicionamento e documente).
- **Kirsch:** 8 máscaras (rotações de 45°), resposta final = máximo por pixel.
- **Laplaciano:** respostas negativas → compare `clamp`, `modulo` e `normalizar` e comente.

### Etapa 3 — Vizinhança
- **Média:** pode chamar a convolução com `ones(n,n)/n²`, ou implementar o laço próprio.
- **Mediana:** laço sobre a janela, ordenar, pegar o central. Não é linear. Será lenta em Python puro: teste em imagens ≤ 256x256 e, se precisar, otimize (acumular a janela em vetor NumPy e usar a ordenação de vetor é aceitável; confirme com o professor).

### Etapa 4 — Histograma
- **Expansão:** `s = (r - min)·255/(max - min)`, tratando `max == min`.
- **Equalização:** histograma → probabilidades → CDF → `round(255·CDF[r])` → LUT aplicada à imagem.
- Mostre o histograma antes/depois (já há um expander na interface).

### Etapa 5 — Aguçamento e contraste adaptativo
- **Laplaciano:** `g = f + c·lap(f)`. Se o centro da máscara é negativo, o realce vem de **subtrair** o Laplaciano (c < 0 na prática). Mostre isso no relatório.
- **High boost:** confira a forma vista em aula e o papel de `A`; `A = 1` recai no aguçamento comum.
- **Contraste adaptativo:** média e desvio padrão locais na janela n x n; trate `σ = 0`.

## 4. Decisões que precisam estar no relatório

| Decisão | Opções | Onde documentar |
|---|---|---|
| Bordas | zeros / replicar / espelhar | 3.3, 4.x, 5 |
| Valores fora de [0,255] | clamp / normalizar / módulo | 3.3, 4.4, 5 |
| Convolução vs correlação | rotacionar ou não a máscara | 3.3.4 |
| Tipo numérico interno | float64 / int32 | 3.1, 3.3 |
| Magnitude do gradiente | √(Gx²+Gy²) vs \|Gx\|+\|Gy\| | 3.3.5 |

A interface já expõe borda e faixa como parâmetros: use isso para **comparar** as opções com a mesma imagem e discutir na seção 5.

## 5. Validar sua implementação (sem violar a regra)

Bibliotecas prontas **não** devem estar no sistema, mas podem servir como **verificação externa** num script de teste separado (`tests/`), nunca importado pelo `core/`:

```python
# tests/test_convolucao.py  (exemplo)
import numpy as np
from scipy.ndimage import correlate     # só para conferir; instale com pip
from core.convolucao import convolver
from core import utils

img = utils.imagem_exemplo()
h = np.array([[0,1,0],[1,-4,1],[0,1,0]], float)
esperado = np.clip(correlate(img.astype(float), h, mode="nearest"), 0, 255).astype(np.uint8)
assert np.abs(convolver(img, h, borda="replicar", faixa="clamp").astype(int) - esperado).max() <= 1
```
Também vale testar matrizes minúsculas (3x3, 5x5) à mão, onde você sabe a resposta.
Confirme com o professor se esse tipo de verificação é permitido.

## 6. Mapa: do sistema para o relatório

| Seção do relatório | O que tirar do projeto |
|---|---|
| 3.1 / 3.2 | Versões do Python/bibliotecas; estrutura de `core/` e `app.py`; diagrama (fluxo: upload → `core` → resultado) |
| 3.3 | Decisões da seção 4 deste guia + trechos curtos de código (poucas linhas) |
| 4.1 | Captura de tela da interface |
| 4.2–4.7 | Aba **Registro de testes** (CSV) + botão **Baixar PNG** para cada resultado |
| 4.4 | Testes obrigatórios do enunciado: aguçamento (vários c, d, incluindo c=d=1), relevo, bordas; informe a soma dos coeficientes (a interface mostra) |
| 5 / 5.1 | Comparações lado a lado, bugs reais que você teve e como resolveu |
| 7 | Declaração de uso de IA (inclua este protótipo e o guia, se os usar) |

**Dica:** use a mesma imagem de teste (idealmente uma com bordas nítidas e outra com ruído) em todas as comparações.

## 7. Melhorias opcionais da interface
- Mostrar `Gx`, `Gy` e magnitude em colunas separadas para Sobel/Roberts/Kirsch (retornar uma tupla de imagens e ajustar o `app.py`).
- Salvar/carregar máscaras personalizadas em JSON.
- Barra de progresso nas operações lentas.
- Modo "comparar": duas operações lado a lado com a mesma entrada.

## 8. Entrega
- `git init`, commits pequenos por funcionalidade, `.gitignore` com `.venv/` e `__pycache__/`.
- `README.md` curto: como instalar e rodar.
- Publique no GitHub e coloque a URL no campo "Repositório" do relatório.
