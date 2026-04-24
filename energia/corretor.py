import os
import json
from ler import ler_simulacao_bin, ler_simulacao_csv
import ncorpos_utilidades as nut
import numpy as np
import matplotlib.pyplot as plt

saida = "euler_corrigido"
diretorio = "../../gravidade-fortran/euler_corrigido/data/"

metodos_plotar = [
  # ["1e4", "1e-4"],
  # ["1e6", "1e-6"],
  ["sem", "Sem correção"],
  ["1e8", r"Corrigido $\varepsilon_C=10^{-8}$"],
]

# plt.figure(figsize=(4,4))

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
  # qs, ps = ler_simulacao_csv(f"{diretorio}/{metodo}/data.csv", 100)
  
  # massas = np.array(massas, dtype=np.longdouble)
  # qs = np.array(qs, dtype=np.longdouble)
  # ps = np.array(ps, dtype=np.longdouble)
  
  # Calcula a energia
  e0 = nut.energia_total(massas, qs[0], ps[0], 1.0, eps)
  energia = [
    abs(nut.energia_total(massas, q, p, 1.0, eps) - e0)
    for (q,p) in zip(qs, ps)
  ]
  # virial = [
  #   nut.virial_potencial_amortecido(massas, q, 1.0, eps) + 2*nut.energia_cinetica(massas, p)
  #   for (q,p) in zip(qs, ps)
  # ]
  # inercia = [
  #   nut.momento_inercia(massas, q) for q in qs
  # ]
  # potencial = [
  #   nut.energia_potencial(massas, q, 1.0, eps) for q in qs
  # ]
  # Cs = [
  #   np.sqrt(I)*abs(V) for I, V in zip(inercia, potencial)
  # ]
  
  ts = np.linspace(0,tf,len(qs))
  
  # plt.plot(ts, np.sqrt(ts)*energia[-1]/np.sqrt(tf), c='black', linestyle='--')  
  plt.plot(ts, energia, label=legenda)
  # plt.plot(ts, virial, label=legenda)

plt.ylabel(r"$\log_{10}{|E(t) - E_0|}$")
# plt.ylabel(r"$2 T(p) + \sum \langle F_a(q), q_a \rangle$")
plt.xlabel(r"$t$")
plt.suptitle("Log-erro absoluto da energia total")

plt.title("Lemniscata, $dt = 10^{-3}$.")
# plt.title("Problema de 700 corpos, $dt = 10^{-3}$.")
plt.yscale("log")
plt.legend()
plt.tight_layout()
# plt.legend(loc='lower left')
plt.savefig(f"{saida}.png")
