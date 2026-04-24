import matplotlib.pyplot as plt
from funcoes import *

img1 = "coloquinho.png"
img2 = "semapinho_pintado.png"
dt = np.pi/4

titulos = [
    "Euler Explícito",
    "Euler Implícito",
    "Euler Simplético"
]
metodos = [
    euler_explicito, euler_implicito, euler_simpletico
]

arquivo = "eulers"

fig, axs = plt.subplots(3, 1, figsize=(8, 10))

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

    # Plotando as imagens

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
    plotar_imagem_pendulo(ax, verlet, dt / 10, arr2_bitmap, cx, cy, raio, tfs)

    # direita
    cx, cy = 2*np.pi, 1.0
    raio = 0.6
    tfs = [i*dt for i in range(6, -1, -1)]
    plotar_imagem_pendulo(ax, metodo, dt, arr2, cx, cy, raio, tfs)

    # ax.set_title(titulo)
    ax.text(-0.8, -1.7, titulo, fontsize=18, color='black', bbox=dict(facecolor='white'))

plt.tight_layout()
plt.savefig(arquivo + ".png")
plt.show()