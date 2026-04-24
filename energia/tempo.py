import os
import json
from ler import ler_simulacao_bin, ler_simulacao_csv
import ncorpos_utilidades as nut
import numpy as np
import matplotlib.pyplot as plt

# Renomeando
# pastas = os.listdir("data")
# for pasta in pastas:
#   # Abre o arquivo de valores iniciais para pegar o metodo
#   with open(f"data/{pasta}/vi.json", 'r') as arq:
#     json_obj = json.load(arq)
#   metodo = json_obj['integracao']['metodo']
#   os.system(f"mv data/{pasta} data/{metodo}")

# exit()

saida = "tempo"
# diretorio = "data"
diretorio = "../../gravidade-fortran/tempo/data/"

# metodos_plotar = [
#   ["euler_exp", "E.E."],
#   ["euler_imp", "E.I."],
#   ["rungekutta2", "RK2"],
#   ["rungekutta3", "RK3"],
#   ["rungekutta4", "RK4"],

#   ["ab2", "AB2"],
#   ["ab3", "AB3"],
#   ["ab4", "AB4"],
#   ["ab5", "AB5"],

#   ["euler_simp", "E.S."],
#   ["verlet", "Verlet"],
#   ["ruth3", "Ruth 3"],
#   ["ruth4", "Ruth 4"],
#   ["ecp4s5", "ecp4s5"],
#   ["ecp4s6", "ecp4s6"],
#   ["rkn551", "RKN551"],
#   ["rkn671", "RKN671"],
#   ["svcp6s9", "svcp6s9"],
#   ["svcp8s15", "svcp8s15"],
#   ["svcp10s35", "svcp10s35"],
# ]

metodos_plotar = [
  [
    ["euler_exp", "E.E."],
    ["euler_imp", "E.I."],
    ["euler_simp", "E.S."],
  ],
  [
    ["ab2", "AB2"],
    ["rungekutta2", "RK2"],
    ["verlet", "Verlet"],
  ],
  [
    ["ab3", "AB3"],
    ["rungekutta3", "RK3"],
    ["ruth3", "Ruth 3"],
  ],
  [
    ["ab4", "AB4"],
    ["rungekutta4", "RK4"],
    ["ruth4", "Ruth 4"],
    ["ecp4s5", "ecp4s5"],
    ["ecp4s6", "ecp4s6"],
  ],
  [
    ["ab5", "AB5"],
    ["rkn551", "RKN551"],
  ],
  [
    ["rkn671", "RKN671"],
    ["svcp6s9", "svcp6s9"],
  ],
  [
    ["svcp8s15", "svcp8s15"],
  ],
  [
    ["svcp10s35", "svcp10s35"],
  ]
]
labels = []

# plt.figure(figsize=(4,7))
j = 0
for grupo in metodos_plotar:
  for i, [metodo, legenda] in enumerate(grupo):
    j += 1
    with open(f"{diretorio}/{metodo}/info.txt", "r") as arq:
      linha_dur = arq.read().split("\n")[-2]
      if "duracao" not in linha_dur:
        linha_dur = arq.read().split("\n")[-1]
      
      duracao = float(linha_dur.split(" ")[-1])
    labels.append([j, metodo])
    plt.bar(j, duracao)
  j += 1

plt.xticks(*list(zip(*labels)))
plt.xticks(rotation=90)
plt.ylabel("Tempo")
plt.xlabel("Método")
plt.suptitle("Tempo computacional de cada método")
# plt.title("Lemniscata, $dt = 10^{-3}$.")
plt.title("$N=500$, $dt = 10^{-2}$, $10^{-1}$, $[0,10]$")
plt.tight_layout()
# plt.yscale("log")
# plt.ylim(1e-16, 1e-1)
# plt.legend(loc='lower left')
plt.savefig(f"{saida}.png")
