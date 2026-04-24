import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Criando a figura e o eixo
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')  # Mantém os círculos redondos de verdade
ax.axis(False)

# Criando os círculos com raio
m1, raio1 = 1.0, 0.5
m2, raio2 = 8/5, 0.8

q = np.array([[3,5], [8,5]])
p = np.array([[0.1*m1,0], [-0.01*m2,0]])

circulo1 = Circle(q[0], raio1, color='blue')
circulo2 = Circle(q[1], raio2, color='red')

ax.add_patch(circulo1)
ax.add_patch(circulo2)

dt = 0.5

def colisao ():
    global q, p, raio1, raio2, m1, m2

    dist = np.linalg.norm(q[0] - q[1])
    if dist > raio1 + raio2 or (q[1]-q[0])@(p[1]-p[0]) > 0:
        return

    N = q[1] - q[0]
    N2 = N @ N

    u1 = p[0] @ N / m1
    u2 = p[1] @ N / m2

    k = 2.0 * (u2 - u1) * m1 * m2 / ((m1 + m2)*N2)

    p[0] = p[0] + k * N
    p[1] = p[1] - k * N
    

# Função de atualização da animação
def atualizar(frame):
    global q,p

    q = q + dt * p
    colisao()

    # Movimento linear horizontal
    circulo1.center = q[0]
    circulo2.center = q[1]
    return circulo1, circulo2

# Criando animação
plt.tight_layout()
anim = FuncAnimation(fig, atualizar, frames=100, interval=1)
anim.save("animacao1.gif", writer="pillow", fps=30)