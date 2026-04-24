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

saida = "lemniscata_metodos_multipasso"
# diretorio = "data"
diretorio = "../../gravidade-fortran/energia400/data/"

metodos_plotar = [
  # ["euler_exp", "E.E."],
  # ["euler_imp", "E.I."],
  # ["rungekutta2", "RK2"],
  # ["rungekutta3", "RK3"],
  # ["rungekutta4", "RK4"],
  
  ["ab2", "AB2"],
  ["ab3", "AB3"],
  ["ab4", "AB4"],
  ["ab5", "AB5"],
  
  # ["euler_simp", "E.S."],
  # ["verlet", "Verlet"],
  # ["ruth3", "Ruth 3"],
  # ["ruth4", "Ruth 4"],
  # ["ecp4s5", "ecp4s5"],
  # ["ecp4s6", "ecp4s6"],
  # ["rkn551", "RKN551"],
  # ["rkn671", "RKN671"],
  # ["svcp6s9", "svcp6s9"],
  # ["svcp8s15", "svcp8s15"],
  # ["svcp8s15", "svcp8s17"],
  # ["svcp10s35", "svcp10s35"],
]

# plt.figure(figsize=(4,7))

for metodo, legenda in metodos_plotar:
  # Abre o arquivo de valores iniciais para pegar massas, eps e tf
  with open(f"{diretorio}/{metodo}/vi.json", 'r') as arq:
    json_obj = json.load(arq)
  massas = json_obj['valores_iniciais']['massas']
  eps = json_obj['integracao']['amortecedor']
  tf = json_obj['integracao']['tf']
  dt = json_obj['integracao']['timestep']
  
  # Agora abre o data.bin para calcular a energia
  # qs, ps = ler_simulacao_bin(f"{diretorio}/{metodo}/data.bin")
  qs, ps = ler_simulacao_csv(f"{diretorio}/{metodo}/data.csv", 100)
  
  massas = np.array(massas, dtype=np.longdouble)
  qs = np.array(qs, dtype=np.longdouble)
  ps = np.array(ps, dtype=np.longdouble)
  
  # Calcula a energia
  e0 = nut.energia_total(massas, qs[0], ps[0], 1.0, eps)
  energia = [
    abs(nut.energia_total(massas, q, p, 1.0, eps) - e0)
    for (q,p) in zip(qs, ps)
  ]
  
  ts = np.linspace(0,tf,len(energia))
  
  # plt.plot(ts, np.sqrt(ts)*energia[-1]/np.sqrt(tf), c='black', linestyle='--')  
  plt.plot(ts, energia, label=legenda)

plt.ylabel(r"$\log_{10}{|E(t) - E_0|}$")
plt.xlabel(r"$t$")
plt.suptitle("Log-erro absoluto da energia total")
# plt.title("Lemniscata, $dt = 10^{-3}$.")
plt.title("Lemniscata, $dt = 10^{-3}$.")
plt.yscale("log")
plt.ylim(1e-16, 1e-1)
plt.legend(loc='lower left')
plt.savefig(f"{saida}.png")
