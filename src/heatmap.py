import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

classes = ["Boa", "Excesso", "Ponte", "Falta", "Fria"]
cm = np.array([
    [486,  22,   4,   6,   2],
    [ 16, 150,   8,   3,   3],
    [  5,   9, 118,   3,   5],
    [  7,   2,   3,  73,   5],
    [  6,   2,   4,   8,  50]
])

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=classes, yticklabels=classes)
plt.xlabel("Classe Prevista")
plt.ylabel("Classe Real")
plt.title("Matriz de Confusão — Inspeção de Soldas PTH (1000 pontos)")
plt.show()