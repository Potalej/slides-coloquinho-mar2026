import os
import json
from ler import ler_simulacao_bin
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

# saida = "lemniscata_metodos_passo_unico_trajetoria"
# metodos_plotar = [
#   ["euler_exp", "E.E."],
#   ["euler_imp", "E.I."],
#   ["rungekutta2", "RK2"],
#   ["rungekutta3", "RK3"],
#   ["rungekutta4", "RK4"],
# ]

saida = "euler_corrigido_trajetorias"
diretorio = "../../gravidade-fortran/euler_corrigido/data/"
metodos_plotar = [
  ["sem", "Sem correção"],
  ["1e8", r"Corrigido $\varepsilon_C=10^{-8}$"],
]

fig, ax = plt.subplots()
plt.grid(True)

for metodo, legenda in metodos_plotar:
  # Abre o arquivo de valores iniciais para pegar massas, eps e tf
  with open(f"{diretorio}/{metodo}/vi.json", 'r') as arq:
    json_obj = json.load(arq)
  massas = json_obj['valores_iniciais']['massas']
  eps = json_obj['integracao']['amortecedor']
  tf = json_obj['integracao']['tf']
  dt = json_obj['integracao']['timestep']
  
  # Agora abre o data.bin para calcular a energia
  qs, ps = ler_simulacao_bin(f"{diretorio}/{metodo}/data.bin")
  
  q_corpos = list(zip(*qs))
  p_corpos = list(zip(*ps))
  q, p = q_corpos[0], p_corpos[0]
  x,y,z = list(zip(*q))

  ax.plot(x,y, label=legenda)
  ax.scatter(x[0],y[0],c='black',zorder=10)
  ax.scatter(x[-1],y[-1],c='red',zorder=10)

ax.set_aspect("equal")
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)
plt.suptitle("Trajetória do corpo 1")
plt.title("Lemniscata, $dt = 10^{-3}$.")
plt.legend()
plt.tight_layout()
plt.savefig(f"{saida}.png")
