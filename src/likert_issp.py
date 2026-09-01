"""
Gráfico de barras empilhadas divergentes (escala Likert)
========================================================

Exemplo baseado no International Social Survey Programme (ISSP, 2009),
módulo "Social Inequality". Pergunta apresentada aos participantes:

    "É responsabilidade do governo reduzir as diferenças de renda
     entre pessoas de alta e de baixa renda."

As respostas foram agrupadas em quatro faixas — Discordo totalmente,
Discordo, Concordo e Concordo totalmente — e são empilhadas a partir de
uma linha de base central: discordâncias para a esquerda, concordâncias
para a direita.

OBS.: os microdados do ISSP 2009 exigem cadastro no GESIS Data Archive
(ZA5400) e não podem ser baixados automaticamente. Os valores usados aqui
são SINTÉTICOS, construídos apenas para reproduzir a ordem de grandeza e o
ordenamento entre países observados na pesquisa original. Eles ficam no
arquivo `likert_issp.csv`, ao lado deste script — para usar os dados reais,
basta substituir o conteúdo do CSV mantendo o mesmo cabeçalho.

Autor: exemplo didático — Visualização Científica (PPGMC/UESC)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# ---------------------------------------------------------------------
# 1. Leitura dos dados (percentuais por país, somando 100% em cada linha)
# ---------------------------------------------------------------------
CATEGORIAS = ["Discordo totalmente", "Discordo", "Concordo", "Concordo totalmente"]
NEGATIVAS = ["Discordo totalmente", "Discordo"]   # empilhadas à esquerda
POSITIVAS = ["Concordo", "Concordo totalmente"]   # empilhadas à direita

ARQUIVO_DADOS = Path(__file__).with_name("likert_issp.csv")

dados = pd.read_csv(
    ARQUIVO_DADOS,
    comment="#",          # ignora as linhas de cabeçalho documental do CSV
    index_col="pais",
    encoding="utf-8",
)
dados = dados[CATEGORIAS]  # garante a ordem das faixas de resposta

# Conferência: cada linha deve somar 100%
assert np.allclose(dados.sum(axis=1), 100), "As linhas devem somar 100%"

# Ordena do maior para o menor grau de concordância; o país com maior
# concordância fica no topo do eixo vertical (barh cresce de baixo p/ cima).
ordem = dados[POSITIVAS].sum(axis=1).sort_values(ascending=True).index
dados = dados.loc[ordem]

# ---------------------------------------------------------------------
# 2. Estilo — cinzas para discordância, laranjas para concordância
# ---------------------------------------------------------------------
CORES = {
    "Discordo totalmente": "#4d4d4d",
    "Discordo":            "#bdbdbd",
    "Concordo":            "#f6b26b",
    "Concordo totalmente": "#d1610a",
}
# Alternativa divergente segura para daltonismo (BrBG):
# CORES = {"Discordo totalmente": "#8c510a", "Discordo": "#dfc27d",
#          "Concordo": "#80cdc1", "Concordo totalmente": "#01665e"}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Calibri", "Carlito", "DejaVu Sans"],
    "font.size": 11,
    "text.color": "#333333",
})


def rotulo(ax, x, y, valor, cor_fundo):
    """Escreve o percentual no centro do segmento, se houver espaço."""
    if valor < 6:                      # segmentos estreitos ficam sem rótulo
        return
    claro = cor_fundo in ("#4d4d4d", "#d1610a", "#8c510a", "#01665e")
    ax.text(x, y, f"{valor:.0f}", ha="center", va="center",
            fontsize=9, color="white" if claro else "#333333")


# ---------------------------------------------------------------------
# 3. Construção do gráfico
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.6))
y = np.arange(len(dados))
altura = 0.68

# --- lado esquerdo (discordância): empilha de dentro para fora ---------
borda = np.zeros(len(dados))
for categoria in NEGATIVAS[::-1]:      # "Discordo" junto ao eixo, depois "Discordo totalmente"
    valor = dados[categoria].to_numpy()
    ax.barh(y, -valor, left=borda, height=altura,
            color=CORES[categoria], edgecolor="white", linewidth=0.8)
    for yi, (b, v) in enumerate(zip(borda, valor)):
        rotulo(ax, b - v / 2, yi, v, CORES[categoria])
    borda = borda - valor

# --- lado direito (concordância) --------------------------------------
borda = np.zeros(len(dados))
for categoria in POSITIVAS:            # "Concordo" junto ao eixo, depois "Concordo totalmente"
    valor = dados[categoria].to_numpy()
    ax.barh(y, valor, left=borda, height=altura,
            color=CORES[categoria], edgecolor="white", linewidth=0.8)
    for yi, (b, v) in enumerate(zip(borda, valor)):
        rotulo(ax, b + v / 2, yi, v, CORES[categoria])
    borda = borda + valor

# --- linha de base central --------------------------------------------
ax.axvline(0, color="#333333", linewidth=1.1, zorder=3)

# ---------------------------------------------------------------------
# 4. Eixos, grade e anotações
# ---------------------------------------------------------------------
ax.set_yticks(y)
ax.set_yticklabels(dados.index)
ax.set_ylim(-0.6, len(dados) - 0.4)

ticks = np.arange(-60, 101, 20)
ax.set_xticks(ticks)
ax.set_xticklabels([f"{abs(t)}%" for t in ticks])   # eixo em valores absolutos
ax.set_xlim(-62, 102)

ax.xaxis.grid(True, color="#e6e6e6", linewidth=0.8)
ax.set_axisbelow(True)
ax.yaxis.grid(False)
ax.tick_params(axis="both", length=0)
for lado in ("top", "right", "left", "bottom"):
    ax.spines[lado].set_visible(False)

ax.set_title(
    "Espanhóis e italianos são os que mais atribuem ao governo o papel\n"
    "de reduzir a desigualdade de renda",
    loc="left", fontsize=15, fontweight="bold", pad=34, color="#222222",
)
ax.text(0, 1.045,
        '"É responsabilidade do governo reduzir as diferenças de renda '
        'entre pessoas de alta e de baixa renda."',
        transform=ax.transAxes, fontsize=10.5, style="italic", color="#666666")

# Legenda na ordem de leitura do gráfico: da discordância à concordância
handles = [Patch(facecolor=CORES[c], label=c) for c in CATEGORIAS]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.19),
          ncol=4, frameon=False, handlelength=1.1, handleheight=1.1,
          columnspacing=1.6, fontsize=10)

fig.text(0.125, -0.02,
         "Fonte: dados sintéticos inspirados no International Social Survey "
         "Programme (ISSP), 2009.",
         fontsize=8.5, color="#8c8c8c")

fig.tight_layout()
fig.savefig("likert_issp.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
