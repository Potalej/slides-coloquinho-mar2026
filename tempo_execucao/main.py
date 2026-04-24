import matplotlib.pyplot as plt

metodos = [
  ("euler_simp",(0, -15) ),
  ("verlet",    (0, 10) ),
  ("ruth3",     (0,-15) ),
  ("ruth4",     (0, 10) ),
  ("rkn551",    (0, 5) ),
  ("rkn671",    (0, 5) ),
  ("svcp8s15",  (0, -15) ),
  ("svcp10s35", (0, 5),),
  ("ab2",       (0, -15) ),
  ("ab3",       (0, 10) ),
  ("ab4",       (0, -15) ),
  ("ab5",       (0,-15) ),
  ("rungekutta2",(0,5) ),
  ("rungekutta3",(0,5) ),
  ("rungekutta4",(0,-15) ),
]

tempos = []

for i, (metodo, xytext) in enumerate(metodos):
  arquivo = f"relatorios/relatorio_{metodo}.txt"
  with open(arquivo, 'r') as arq:
    texto = arq.read()
  linhas = texto.split('\n')
  
  interesse1 = linhas[5]
  t1 = float(interesse1[:10].strip())
  
  interesse2 = linhas[6]
  t2 = float(interesse2[:10].strip())
  
  plt.scatter(i, t1, label=metodo)
  plt.annotate(metodo, # This is the text
              (i, t1), # This is the point to annotate (xy)
              textcoords="offset points", # How to position the text
              xytext=xytext, # Distance from the point (x, y)
              ha='center') # Horizontal alignment of the text

# plt.legend()
plt.suptitle("Proporção do tempo na rotina de forças vs rotina do método", fontsize=14)
plt.title(r"$N=20, \ dt = 10^{-4}, \ t_f = 100, \ \varepsilon = 0.05$", fontsize=10)
plt.xlabel("% Tempo na rotina de forças")
plt.ylabel("% Tempo na rotina do método")
plt.tight_layout()
plt.savefig("teste.png")
plt.close()
