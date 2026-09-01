"""
Barras empilhadas com Matplotlib - material de apoio
Visualizacao Cientifica / PPGMC - UESC

Gera quatro figuras a partir de tres arquivos CSV:

  fig1  empilhado com totais VARIAVEIS      (tempos_execucao_paralela.csv, formato longo)
  fig2  empilhado 100% do MESMO dado        (mostra a mudanca de composicao)
  fig3  agrupadas x empilhadas lado a lado  (producao_cacau_sintetico.csv, formato largo)
  fig4  empilhado 100% horizontal           (composicao_amostras.csv, linhas somam 100)

Observacao: os tres CSVs contem dados SINTETICOS, criados apenas para fins didaticos.

Uso:  python barras_empilhadas.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# 1. Estilo: "comece com o cinza" - um unico acento de cor
# ----------------------------------------------------------------------

plt.rcParams.update({
    "font.family": ["Calibri", "Carlito", "DejaVu Sans"],  # cai no default se Calibri nao existir
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.dpi": 110,
})

LARANJA = "#E8702A"
GRAFITE = "#3D3D3D"

# Paleta com um destaque: a serie que se quer discutir recebe o laranja,
# as demais ficam em tons de cinza (claro -> escuro).
PALETA_DESTAQUE = [LARANJA, "#9E9E9E", "#BDBDBD", "#DCDCDC"]

# Paleta neutra sequencial, util quando nenhuma serie deve dominar a atencao.
PALETA_NEUTRA = ["#4A4A4A", "#7C7C7C", "#A8A8A8", "#D2D2D2"]


def barras_empilhadas(ax, categorias, series, cores=None, horizontal=False,
                      normalizar=False, largura=0.68, rotulo_total=True,
                      formato_total="{:.0f}"):
    """Desenha um grafico de barras empilhadas.

    categorias : lista de rotulos do eixo categorico (uma barra por item)
    series     : dict {nome_da_serie: array de valores}, na ordem de empilhamento
                 (o primeiro item fica na base da barra)
    normalizar : True converte cada barra para 100% (composicao)
    """
    nomes = list(series.keys())
    M = np.array([series[n] for n in nomes], dtype=float)   # (n_series, n_categorias)
    totais = M.sum(axis=0)

    if normalizar:
        M = M / totais * 100.0

    cores = cores or PALETA_NEUTRA
    pos = np.arange(len(categorias))
    base = np.zeros(len(categorias))                        # acumulador do empilhamento

    for i, nome in enumerate(nomes):
        cor = cores[i % len(cores)]
        if horizontal:
            ax.barh(pos, M[i], left=base, height=largura, label=nome,
                    color=cor, edgecolor="white", linewidth=0.8)
        else:
            ax.bar(pos, M[i], bottom=base, width=largura, label=nome,
                   color=cor, edgecolor="white", linewidth=0.8)
        base += M[i]                                        # a chave do metodo

    if horizontal:
        ax.set_yticks(pos, categorias)
        ax.invert_yaxis()
        ax.xaxis.grid(True, color="#E6E6E6", linewidth=0.8)
        ax.spines["bottom"].set_visible(False)
    else:
        ax.set_xticks(pos, categorias)
        ax.yaxis.grid(True, color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)   # a grade nunca cruza os segmentos empilhados

    ax.tick_params(length=0)

    if rotulo_total and not normalizar:
        for p, t in zip(pos, totais):
            if horizontal:
                ax.text(t * 1.01, p, formato_total.format(t), va="center",
                        ha="left", color=GRAFITE, fontsize=9)
            else:
                ax.text(p, t * 1.02, formato_total.format(t), ha="center",
                        va="bottom", color=GRAFITE, fontsize=9)

    return ax


def legenda_na_ordem_da_pilha(ax, **kw):
    """Inverte a legenda para que ela siga a ordem visual do empilhamento."""
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], frameon=False, **kw)


# ----------------------------------------------------------------------
# 2. Dado em formato LONGO (tidy) -> pivot -> empilhado
# ----------------------------------------------------------------------

longo = pd.read_csv("tempos_execucao_paralela.csv")

# pivot_table transforma o formato longo na matriz categoria x serie
tabela = longo.pivot_table(index="n_processos", columns="etapa", values="tempo_s")
ordem = ["Computacao", "Comunicacao", "Sincronizacao", "Entrada_Saida"]
tabela = tabela[ordem]

categorias = [str(p) for p in tabela.index]
series = {c.replace("_", "/"): tabela[c].to_numpy() for c in tabela.columns}

# --- fig1: totais variaveis -------------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 4.4))
barras_empilhadas(ax, categorias, series, cores=PALETA_DESTAQUE,
                  formato_total="{:.1f}s")
ax.set_title("O tempo total cai ate 8 processos e volta a crescer",
             loc="left", fontsize=13, color=GRAFITE, weight="bold")
ax.set_xlabel("Numero de processos")
ax.set_ylabel("Tempo de execucao (s)")
ax.set_ylim(0, 145)
legenda_na_ordem_da_pilha(ax, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.tight_layout()
fig.savefig("fig1_empilhado_totais_variaveis.png", bbox_inches="tight")

# --- fig2: mesmo dado, normalizado a 100% -----------------------------
fig, ax = plt.subplots(figsize=(7.6, 4.4))
barras_empilhadas(ax, categorias, series, cores=PALETA_DESTAQUE,
                  normalizar=True)
ax.set_title("A computacao sai de 93% para 10% do tempo total",
             loc="left", fontsize=13, color=GRAFITE, weight="bold")
ax.set_xlabel("Numero de processos")
ax.set_ylabel("Participacao no tempo total (%)")
ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
legenda_na_ordem_da_pilha(ax, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.tight_layout()
fig.savefig("fig2_empilhado_100_por_cento.png", bbox_inches="tight")

# ----------------------------------------------------------------------
# 3. Dado em formato LARGO -> agrupadas x empilhadas
# ----------------------------------------------------------------------

largo = pd.read_csv("producao_cacau_sintetico.csv").set_index("municipio")
cat2 = list(largo.index)
ser2 = {c.replace("_", " "): largo[c].to_numpy() for c in largo.columns}

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.4, 4.6), sharey=False)

# (A) barras agrupadas: comparam categorias DENTRO de cada municipio
pos = np.arange(len(cat2))
n = len(ser2)
w = 0.8 / n
for i, (nome, vals) in enumerate(ser2.items()):
    axA.bar(pos + (i - (n - 1) / 2) * w, vals, width=w, label=nome,
            color=PALETA_NEUTRA[i], edgecolor="white", linewidth=0.6)
axA.set_xticks(pos, cat2, rotation=30, ha="right")
axA.yaxis.grid(True, color="#E6E6E6", linewidth=0.8)
axA.set_axisbelow(True)
axA.tick_params(length=0)
axA.set_title("Agrupadas: comparam as partes entre si",
              loc="left", fontsize=12, color=GRAFITE, weight="bold")
axA.set_ylabel("Producao (t)")
axA.legend(frameon=False)

# (B) barras empilhadas: mostram a parte E o total
barras_empilhadas(axB, cat2, ser2, cores=PALETA_NEUTRA)
axB.set_xticks(np.arange(len(cat2)), cat2, rotation=30, ha="right")
axB.set_title("Empilhadas: mostram a parte e o total",
              loc="left", fontsize=12, color=GRAFITE, weight="bold")
axB.set_ylabel("Producao (t)")
axB.set_ylim(0, 4600)
legenda_na_ordem_da_pilha(axB, loc="upper right")

fig.tight_layout()
fig.savefig("fig3_agrupadas_vs_empilhadas.png", bbox_inches="tight")

# ----------------------------------------------------------------------
# 4. Linhas que ja somam 100 -> empilhado horizontal
# ----------------------------------------------------------------------

comp = pd.read_csv("composicao_amostras.csv").set_index("ponto_coleta")
cat3 = list(comp.index)
ser3 = {c.replace("_", " "): comp[c].to_numpy() for c in comp.columns}

fig, ax = plt.subplots(figsize=(8.2, 4.2))
barras_empilhadas(ax, cat3, ser3, cores=PALETA_DESTAQUE,
                  horizontal=True, normalizar=True)
ax.set_title("A fracao de areia cai da nascente para a foz",
             loc="left", fontsize=13, color=GRAFITE, weight="bold")
ax.set_xlabel("Composicao granulometrica (%)")
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
legenda_na_ordem_da_pilha(ax, loc="upper center", bbox_to_anchor=(0.5, -0.18),
                          ncols=4)
fig.tight_layout()
fig.savefig("fig4_empilhado_horizontal_100.png", bbox_inches="tight")

print("Figuras geradas com sucesso.")
