import matplotlib.pyplot as plt
from funcoes import *
from time import time
from scipy import special

img2 = "semapinho_pintado.png"
dt = np.pi/4

titulos = [
    "Plot"
]

def exato_2pi (Qn, Pn, dt, n_steps, E0=0.0):
    Q0, P0 = Qn, Pn
    tf = n_steps * dt

    # regime oscilatório
    k2 = E0/2.0
    k = np.sqrt(k2)

    # fase inicial
    sn0 = -np.sin(Q0/2)/k
    u0 = special.ellipkinc(np.arcsin(sn0), k2)

    # evolução temporal
    u = u0 + tf

    sn, cn, dn, ph = special.ellipj(u, k2)

    Qn = 2*np.arcsin(k*sn) + 2*np.pi
    Pn = 2*k*cn*dn

    return Qn, Pn

def euler_explicito_corrigido (Qn, Pn, dt, n_steps, E0):
    for _ in range(n_steps):
        Qn, Pn = euler_explicito(Qn, Pn, dt, 1, E0)
        Qn, Pn = corretor(Qn, Pn, E0)
    return Qn, Pn

def euler_simpletico_corrigido (Qn, Pn, dt, n_steps, E0):
    for _ in range(n_steps):
        Qn, Pn = euler_simpletico(Qn, Pn, dt, 1, E0)
        Qn, Pn = corretor(Qn, Pn, E0)
    return Qn, Pn

# metodos = [
#     euler_explicito, 
#     euler_simpletico,
#     euler_explicito_corrigido,
#     euler_simpletico_corrigido
# ]

arquivo = "so_semapinho"

# fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig, ax = plt.subplots(figsize=(12, 10))

# Plotando o campo
ax = plotar_campo(ax)

# Abrindo as imagens
arr2 = abrir_imagem(img2)
arr2_bitmap = abrir_imagem("semapinho_pintado.png")

tempo = time()

# direita - bitmap
cx, cy = 0, 1.8
raio = 1.0
tfs = [i*dt for i in range(3, -1, -1)]
plotar_imagem_pendulo(ax, rk4, dt/30, arr2_bitmap, cx, cy, raio, tfs)

# ax.set_xlim(-np.pi/2,1.5*np.pi)
plt.tight_layout()
plt.savefig(arquivo + ".png")
plt.show()