import os
import json
from ler import ler_simulacao_bin
import ncorpos_utilidades as nut
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

saida = "lemniscata_video"
metodos_plotar = [
  ["rungekutta4", "RK4"],
]

for metodo, legenda in metodos_plotar:
  # Abre o arquivo de valores iniciais para pegar massas, eps e tf
  with open(f"data/{metodo}/vi.json", 'r') as arq:
    json_obj = json.load(arq)
  massas = json_obj['valores_iniciais']['massas']
  eps = json_obj['integracao']['amortecedor']
  tf = json_obj['integracao']['tf']
  dt = json_obj['integracao']['timestep']
  
  # Agora abre o data.bin para calcular a energia
  pos, ps = np.array(ler_simulacao_bin(f"data/{metodo}/data.bin"))
  pos = pos[:800]
  
  # pos.shape = (M, N, 3)
  M, N, _ = pos.shape

  fig, ax = plt.subplots()

  # limites fixos (evita tremida)
  xmin, xmax = -1.5,1.5
  ymin, ymax = -0.5,0.5

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)
  ax.set_aspect('equal')

  # pontos atuais
  scat = ax.scatter([], [], s=30)

  # linhas de rastro (uma por corpo)
  trails = [ax.plot([], [], lw=1, alpha=0.6)[0] for _ in range(N)]

  def update(frame):
      # Atualiza posição atual
      scat.set_offsets(pos[frame, :, :2])
      
      # Atualiza rastros
      for i in range(N):
        
        rastro = 30 if frame >= 30 else frame
          
        trails[i].set_data(
            pos[frame-rastro:frame+1, i, 0],
            pos[frame-rastro:frame+1, i, 1]
        )
          
      return [scat] + trails

  ani = FuncAnimation(fig, update, frames=M, interval=40)
  plt.tight_layout()
  plt.suptitle("Lemniscata via RK4 com $dt=10^{-3}$ no intervalo $[0, 20]$")
  ani.save("simulacao_2d.gif", writer="pillow", fps=25)