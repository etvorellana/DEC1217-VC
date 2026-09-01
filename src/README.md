# Barras empilhadas — conjunto de dados e código de apoio

Material didático para a aula sobre gráficos de barras. **Todos os dados são sintéticos**,
criados apenas para ilustrar o comportamento das duas variantes do gráfico empilhado.

## Arquivos de dados

| Arquivo | Formato | Total das barras | Serve para mostrar |
|---|---|---|---|
| `tempos_execucao_paralela.csv` | longo (tidy): `n_processos, etapa, tempo_s` | **variável** (129 s → 37 s → 48 s) | empilhado com totais diferentes; exige `pivot_table` antes de plotar |
| `producao_cacau_sintetico.csv` | largo: uma coluna por série | **variável** | agrupadas × empilhadas com os mesmos dados |
| `composicao_amostras.csv` | largo, cada linha soma 100 | **fixo (100 %)** | empilhado de composição; barra horizontal |

O primeiro conjunto é o mais didático: entre 1 e 32 processos o tempo total cai e volta a subir,
enquanto a fração de computação despenca de ~93 % para ~10 %. As duas variantes do gráfico
contam histórias diferentes sobre a **mesma** tabela.

## Código

```bash
python barras_empilhadas.py
```

Gera quatro figuras PNG. A função `barras_empilhadas()` é reutilizável e cobre os quatro casos
(vertical/horizontal, absoluto/normalizado). O mecanismo essencial são três linhas:

```python
base = np.zeros(len(categorias))
for nome, valores in series.items():
    ax.bar(pos, valores, bottom=base, label=nome)
    base += valores          # o topo de um segmento vira a base do próximo
```

Para normalizar a 100 %, basta dividir a matriz pelos totais das colunas antes do laço:
`M = M / M.sum(axis=0) * 100`.

## Pontos de discussão em aula

1. Só o segmento da base e o comprimento total têm linha de referência comum; os segmentos do
   meio "flutuam" e são difíceis de comparar entre barras.
2. Coloque na base a série mais importante ou a mais estável.
3. Limite a cinco ou seis segmentos; acima disso, prefira pequenos múltiplos.
4. Inverta a ordem da legenda para que ela acompanhe a ordem visual da pilha.
5. A versão 100 % descarta a informação de magnitude — combine-a com um rótulo ou um gráfico
   auxiliar do total quando o tamanho importar.
6. Barras empilhadas não admitem valores negativos sem ambiguidade.
