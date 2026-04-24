import matplotlib.pyplot as plt
from funcoes import *
from time import time
from scipy import special

img1 = "coloquinho.png"
img2 = "semapinho_pintado.png"
dt = np.pi/4

titulos = [
    "Euler Explícito",
    "Euler Simplético",
    "Euler Explícito Corrigido",
    "Euler Simplético Corrigido"
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

metodos = [
    euler_explicito, 
    euler_simpletico,
    euler_explicito_corrigido,
    euler_simpletico_corrigido
]

arquivo = "corretor1"

# fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig, ax_s = plt.subplots(2,2, figsize=(12, 10))
axs = [ax_s[0,0], ax_s[1,0], ax_s[0,1], ax_s[1,1]]

for i in range(len(titulos)):
    titulo = titulos[i]
    metodo = metodos[i]
    ax = axs[i]

    # Plotando o campo
    ax = plotar_campo(ax)

    # Abrindo as imagens
    arr1 = abrir_imagem(img1)
    arr1_bitmap = abrir_imagem("coloquinho_bitmap.png")
    arr2 = abrir_imagem(img2)
    arr2_bitmap = abrir_imagem("bitmap.png")

    tempo = time()

    # esquerda - bitmap
    cx, cy = 0, 1.8
    raio = 1.0
    tfs = [i*dt for i in range(3, -1, -1)]
    plotar_imagem_pendulo(ax, rk4, dt / 20, arr1_bitmap, cx, cy, raio, tfs)

    # esquerda
    cx, cy = 0, 1.8
    raio = 1.0
    tfs = [i*dt for i in range(3, -1, -1)]
    plotar_imagem_pendulo(ax, metodo, dt, arr1, cx, cy, raio, tfs)

    # direita - bitmap
    cx, cy = 2*np.pi, 1.0
    raio = 0.6
    tfs = [i*dt for i in range(6, -1, -1)]
    plotar_imagem_pendulo(ax, exato_2pi, dt, arr2_bitmap, cx, cy, raio, tfs)

    # direita
    cx, cy = 2*np.pi, 1.0
    raio = 0.6
    tfs = [i*dt for i in range(6, -1, -1)]
    plotar_imagem_pendulo(ax, metodo, dt, arr2, cx, cy, raio, tfs)

    print(f"Tempo ({titulo}): {time() - tempo}")

    # ax.set_title(titulo)
    ax.text(-0.8, -1.7, titulo, fontsize=18, color='black', bbox=dict(facecolor='white'))

plt.tight_layout()
plt.savefig(arquivo + ".png")
plt.show()