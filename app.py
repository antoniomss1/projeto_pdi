"""Protótipo de interface - Sistema de Processamento de Imagens (UNIR / PDI).

Execute com:  streamlit run app.py
"""
import io

import numpy as np
import pandas as pd
import streamlit as st

from core import (agucamento, bordas, contraste_adaptativo, convolucao,
                  histograma, intensidade, utils, vizinhanca)

st.set_page_config(page_title="Processamento de Imagens · UNIR", page_icon="🖼️",
                   layout="wide")

# Máscaras de EXEMPLO. Substitua/complete com as máscaras exigidas no enunciado.
PRESETS = {
    "Personalizada": None,
    "Média 3x3 (1/9)": np.ones((3, 3)) / 9,
    "Sobel Gx": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float),
    "Sobel Gy": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], float),
    "Laplaciano 4-viz.": np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float),
    "Laplaciano 8-viz.": np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], float),
    "Aguçamento (exemplo)": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], float),
    "Relevo (exemplo)": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], float),
}

ss = st.session_state
ss.setdefault("fonte", None)
ss.setdefault("original", None)
ss.setdefault("resultado", None)
ss.setdefault("registro", [])


# ------------------------------------------------------------ utilitários
@st.cache_data(show_spinner=False)
def hist_cache(img):
    return histograma.calcular_histograma(img)


def para_png(arr):
    buf = io.BytesIO()
    utils.para_pil(arr).save(buf, format="PNG")
    return buf.getvalue()


def resumir(v):
    if isinstance(v, np.ndarray):
        return v.tolist() if v.ndim == 2 and v.size <= 121 else f"imagem {v.shape}"
    return v


def ui_borda_faixa(faixa_padrao="clamp"):
    c1, c2 = st.columns(2)
    borda = c1.selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1)
    faixa = c2.selectbox("Valores fora de [0,255]", utils.MODOS_FAIXA,
                         index=utils.MODOS_FAIXA.index(faixa_padrao))
    return borda, faixa


# --------------------------------------------- parâmetros de cada operação
def ui_intensidade(op, ent):
    if op == "Negativo":
        return intensidade.negativo, {}
    if op == "Limiarização":
        return intensidade.limiarizacao, {"T": st.slider("Limiar T", 0, 255, 128)}
    if op == "Alargamento de contraste":
        c = st.columns(4)
        r1 = c[0].slider("r1", 0, 255, 70)
        s1 = c[1].slider("s1", 0, 255, 20)
        r2 = c[2].slider("r2", 0, 255, 180)
        s2 = c[3].slider("s2", 0, 255, 235)
        if r1 >= r2:
            st.warning("Use r1 < r2.")
        return intensidade.alargamento_contraste, dict(r1=r1, s1=s1, r2=r2, s2=s2)
    if op == "Gamma":
        c = st.columns(2)
        return intensidade.gamma, dict(
            c=c[0].slider("c", 0.1, 2.0, 1.0, 0.05),
            gamma=c[1].slider("γ (gamma)", 0.1, 5.0, 0.5, 0.05))
    if op == "Logaritmo":
        return intensidade.logaritmo, {"c": st.slider("c", 1.0, 100.0, 46.0, 0.5)}
    if op == "Dissolve":
        modo = st.radio("Tipo", ["Uniforme", "Não uniforme"], horizontal=True)
        outra = st.file_uploader("Segunda imagem", type=["png", "jpg", "jpeg", "bmp"],
                                 key="img_b")
        if outra is not None:
            img_b = utils.carregar_cinza_redimensionada(outra, ent.shape)
        else:
            st.info("Sem segunda imagem: usando a própria imagem espelhada.")
            img_b = np.fliplr(ent).copy()
        if modo == "Uniforme":
            return intensidade.dissolve_uniforme, dict(
                img_b=img_b, alpha=st.slider("α", 0.0, 1.0, 0.5, 0.05))

        img_t = st.file_uploader("imagem de transição", type=["png", "jpg", "jpeg", "bmp"], key="img_t")

        if img_t is not None:
            img_t = utils.carregar_cinza_redimensionada(img_t, ent.shape)
        else:
            st.info("Sem imagem de transição: usando a própria imagem espelhada.")
            img_t = np.fliplr(ent).copy()
        
        return intensidade.dissolve_nao_uniforme, dict(
            img_b=img_b, img_t=img_t)


def ui_histograma(op, ent):
    return (histograma.expandir if op == "Expansão" else histograma.equalizar), {}


def ui_vizinhanca(op, ent):
    n = st.slider("Tamanho da janela n (n x n)", 3, 15, 3, 2)
    borda = st.selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1)
    f = vizinhanca.media if op == "Média" else vizinhanca.mediana
    return f, dict(n=n, borda=borda)


def ui_convolucao(op, ent):
    preset = st.selectbox("Máscara pré-definida (exemplos)", list(PRESETS))
    if PRESETS[preset] is None:
        c = st.columns(2)
        n = c[0].number_input("Linhas (n)", 1, 11, 3)
        m = c[1].number_input("Colunas (m)", 1, 11, 3)
        base = np.zeros((n, m))
        base[n // 2, m // 2] = 1.0
    else:
        base = PRESETS[preset]
    df = st.data_editor(pd.DataFrame(base), key=f"mask_{preset}_{base.shape}",
                        hide_index=True, width="content")
    mascara = df.to_numpy(dtype=float)
    st.caption(f"Soma dos coeficientes: **{mascara.sum():.4g}** "
               f"({mascara.shape[0]}x{mascara.shape[1]})")
    c = st.columns(3)
    offset = c[0].number_input("Offset", -255, 255, 0)
    borda = c[1].selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1)
    faixa = c[2].selectbox("Valores fora de [0,255]", utils.MODOS_FAIXA)
    return convolucao.convolver, dict(mascara=mascara, offset=offset,
                                      borda=borda, faixa=faixa)


def ui_bordas(op, ent):
    kw = {}
    if op in ("Roberts", "Sobel"):
        kw["metodo"] = st.radio("Magnitude", ["raiz", "soma_abs"], horizontal=True,
                                format_func=lambda v: "√(Gx²+Gy²)" if v == "raiz"
                                else "|Gx|+|Gy|")
    if op == "Laplaciano":
        kw["variante"] = st.radio("Máscara", ["4-vizinhos", "8-vizinhos"], horizontal=True)
    borda, faixa = ui_borda_faixa("normalizar")
    kw.update(borda=borda, faixa=faixa)
    f = dict(Roberts=bordas.roberts, Sobel=bordas.sobel,
             Kirsch=bordas.kirsch, Laplaciano=bordas.laplaciano)[op]
    return f, kw


def ui_agucamento(op, ent):
    if op == "Laplaciano":
        c = st.columns(2)
        kw = dict(c=c[0].number_input("c", -5.0, 5.0, 1.0, 0.1),
                  variante=c[1].radio("Máscara", ["4-vizinhos", "8-vizinhos"],
                                      horizontal=True))
        kw["borda"] = st.selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1)
        return agucamento.agucar_laplaciano, kw
    c = st.columns(3)
    return agucamento.high_boost, dict(
        A=c[0].number_input("A", 1.0, 10.0, 1.5, 0.1),
        n=c[1].slider("Janela da suavização n", 3, 15, 3, 2),
        borda=c[2].selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1))


def ui_contraste(op, ent):
    c = st.columns(3)
    return contraste_adaptativo.contraste_adaptativo, dict(
        c=c[0].number_input("c", 0.0, 100.0, 1.0, 0.1),
        n=c[1].slider("Vizinhança n x n", 3, 31, 7, 2),
        borda=c[2].selectbox("Tratamento de borda", utils.MODOS_BORDA, index=1))


GRUPOS = {
    "Intensidade": (["Negativo", "Limiarização", "Alargamento de contraste",
                     "Gamma", "Logaritmo", "Dissolve"], ui_intensidade),
    "Histograma": (["Expansão", "Equalização"], ui_histograma),
    "Filtros de vizinhança": (["Média", "Mediana"], ui_vizinhanca),
    "Convolução genérica": (["Convolução g = f*h + offset"], ui_convolucao),
    "Detecção de bordas": (["Roberts", "Sobel", "Kirsch", "Laplaciano"], ui_bordas),
    "Aguçamento": (["Laplaciano", "High boost"], ui_agucamento),
    "Contraste adaptativo": (["Contraste adaptativo"], ui_contraste),
}

# ------------------------------------------------------------- barra lateral
with st.sidebar:
    st.header("Imagem")
    arquivo = st.file_uploader("Carregar imagem", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"])
    fonte = f"{arquivo.name}-{arquivo.size}" if arquivo else "exemplo"
    if ss.fonte != fonte:
        ss.fonte = fonte
        ss.original = utils.carregar_cinza(arquivo) if arquivo else utils.imagem_exemplo()
        ss.resultado = None
    if not arquivo:
        st.caption("Usando imagem sintética de exemplo (com ruído).")
    alt, larg = ss.original.shape
    st.caption(f"{larg}×{alt} px · 8 bits · escala de cinza")

    st.header("Entrada da operação")
    opcoes = ["Imagem original"] + (["Último resultado"] if ss.resultado is not None else [])
    escolha_ent = st.radio("Aplicar sobre", opcoes)
    st.caption("Operações em Python puro podem demorar em imagens grandes.")

entrada = ss.original if escolha_ent == "Imagem original" else ss.resultado

# ----------------------------------------------------------------- principal
st.title("Sistema de Processamento de Imagens")
tab_proc, tab_reg, tab_ajuda = st.tabs(["Processamento", "Registro de testes", "Ajuda"])

with tab_proc:
    c1, c2 = st.columns(2)
    grupo = c1.selectbox("Grupo de operações", list(GRUPOS))
    ops, ui_fn = GRUPOS[grupo]
    op = c2.selectbox("Operação", ops)

    with st.container(border=True):
        st.subheader("Parâmetros")
        func, kwargs = ui_fn(op, entrada)

    b1, b2, _ = st.columns([1, 1, 4])
    if b1.button("Aplicar", type="primary"):
        try:
            with st.spinner("Processando..."):
                ss.resultado = func(entrada, **kwargs)
            ss.registro.append({
                "#": len(ss.registro) + 1,
                "grupo": grupo, "operação": op,
                "parâmetros": str({k: resumir(v) for k, v in kwargs.items()}),
                "entrada": escolha_ent,
                "imagem": "exemplo" if not arquivo else arquivo.name,
            })
        except NotImplementedError as e:
            st.warning(f"🚧 Ainda não implementado: `{e}` — veja o GUIA.md.")
        except Exception as e:  # erros de implementação aparecem sem derrubar a UI
            st.error(f"Erro ao processar: {e}")
    if b2.button("Limpar resultado"):
        ss.resultado = None
        st.rerun()

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Entrada**")
        st.image(entrada, clamp=True, width="stretch")
    with col_b:
        st.markdown("**Resultado**")
        if ss.resultado is None:
            st.info("Escolha uma operação e clique em *Aplicar*.")
        else:
            st.image(ss.resultado, clamp=True, width="stretch")
            st.download_button("Baixar PNG", para_png(ss.resultado),
                               file_name="resultado.png", mime="image/png")

    with st.expander("Histogramas"):
        h1, h2 = st.columns(2)
        h1.bar_chart(pd.DataFrame({"frequência": hist_cache(entrada)}), height=200)
        if ss.resultado is not None:
            h2.bar_chart(pd.DataFrame({"frequência": hist_cache(ss.resultado)}), height=200)

with tab_reg:
    st.markdown("Cada *Aplicar* bem-sucedido é registrado aqui — use como base "
                "para as legendas e tabelas de parâmetros do relatório.")
    if ss.registro:
        df = pd.DataFrame(ss.registro)
        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button("Baixar CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name="registro_testes.csv", mime="text/csv")
        if st.button("Limpar registro"):
            ss.registro = []
            st.rerun()
    else:
        st.info("Nenhum teste registrado ainda.")

with tab_ajuda:
    st.markdown("""
**Como usar:** carregue uma imagem (ou use a de exemplo) → escolha grupo e operação →
ajuste os parâmetros → *Aplicar*. Marque *Último resultado* na barra lateral para encadear operações.

**Status do protótipo:** a interface está completa. Estão implementadas apenas as
transformações de intensidade e o cálculo do histograma; as demais operações exibem
um aviso 🚧 até você implementá-las em `core/`. O passo a passo está no `GUIA.md`.
""")
