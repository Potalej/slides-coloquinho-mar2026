import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def abrir_imagem (imagem:str):
    img = Image.open(imagem).convert("RGBA")
    # separar canais
    arr = np.array(img) / 255.0  # normaliza 0..1 para cada canal R,G,B,A

    # pegar menor dimensão
    h, w, _ = arr.shape
    min_side = min(h, w)

    # calcular cortes
    top = (h - min_side) // 2
    bottom = top + min_side
    left = (w - min_side) // 2
    right = left + min_side

    # recortar
    arr = arr[top:bottom, left:right]

    return arr

###########################

def plotar_campo (ax, N=1000):
    q1 = np.linspace(-1.2, np.pi, N)
    q2 = np.linspace(np.pi, 10.5, N)

    p1 = np.linspace(0, 2, N)
    Es = np.linspace(0.1, 2, 7).tolist()
    Es = Es + np.linspace(2, 7, 13).tolist()

    for E in Es:
        cor = 'gray' if E != 2.0 else "black"
        for q in [q1,q2]:
            p = np.sqrt(2*(E - 1 + np.cos(q)))
            ax.plot(q,p, c=cor)
            ax.plot(q,-p, c=cor)
        for p in [p1]:
            q = np.arccos(p*p/2 - E + 1)
            ax.plot(q,p,   c=cor)
            ax.plot(q,-p,  c=cor)
            ax.plot(-q,p,  c=cor)
            ax.plot(-q,-p, c=cor)

            ax.plot( q + 2*np.pi,p,  c=cor)
            ax.plot( q + 2*np.pi,-p, c=cor)
            ax.plot(-q + 2*np.pi,p,  c=cor)
            ax.plot(-q + 2*np.pi,-p, c=cor)

    ax.set_xlim(-1.2, 10.5)
    ax.set_ylim(-2,3)
    ax.axvline(0, c='black')
    ax.axhline(0, c='black')

    return ax


#####################################

def plotar_transformacao (ax, dt, tf, Q, P, arr, metodo, E0):
    n_steps = int(tf / dt)

    Qn = Q.copy()
    Pn = P.copy()

    Qn, Pn = metodo(Qn, Pn, dt, n_steps, E0)

    cores = []
    for i in range(len(Q)-1,-1,-1):
        for j in range(len(P)):
            c = arr[i,j]
            cores.append(c)

    Qn_flat = Qn.ravel()
    Pn_flat = Pn.ravel()

    ax.scatter(Qn_flat,Pn_flat, c=cores, s=1, marker='o',edgecolors='none', rasterized=True, zorder=5)
    return ax

f_q = lambda pn: pn
f_p = lambda qn: - np.sin(qn)
f_p_der = lambda qn: - np.cos(qn)

def euler_explicito (Qn, Pn, dt, n_steps, E0=0.0):
    for _ in range(n_steps):
        Q1 = Qn + dt*f_q(Pn)
        Pn = Pn + dt*f_p(Qn)
        Qn = Q1
    return Qn, Pn

def euler_implicito (Qn, Pn, dt, n_steps, E0=0.0):
    for _ in range(n_steps):
        x = Pn + dt * f_p(Qn)

        for __ in range(10):
            m = x - Pn + dt * np.sin(Qn + dt * x)
            dm = 1 + dt*dt*np.cos(Qn + dt * x)
            delta = m/dm
            x = x - delta
            # if np.all(np.abs(delta) < dt**4):
            #     break
        
        Pn = x
        Qn = Qn + dt*f_q(Pn)
    return Qn, Pn

def euler_simpletico (Qn, Pn, dt, n_steps, E0=0.0):
    for _ in range(n_steps):
        Pn = Pn + dt*f_p(Qn)
        Qn = Qn + dt*f_q(Pn)
    return Qn, Pn

def verlet (Qn, Pn, dt, n_steps, E0=0.0):
    F = f_p(Qn)
    for _ in range(n_steps):
        Pn = Pn + 0.5*dt*F
        Qn = Qn + dt*f_q(Pn)
        F = f_p(Qn)
        Pn = Pn + 0.5*dt*F
    return Qn, Pn

def rk2 (Qn, Pn, dt, n_steps, E0=0.0):
    for _ in range(n_steps):
        k1q = f_q(Pn)
        k1p = f_p(Qn)

        k2q = f_q(Pn + 0.5 * dt * k1p)
        k2p = f_p(Qn + 0.5 * dt * k1q)

        Qn = Qn + 0.5*dt*(k1q + k2q)
        Pn = Pn + 0.5*dt*(k1p + k2p)
    return Qn, Pn

def rk4 (Qn, Pn, dt, n_steps, E0=0.0):
    for _ in range(n_steps):
        k1q = f_q(Pn)
        k1p = f_p(Qn)

        k2q = f_q(Pn + 0.5 * dt * k1p)
        k2p = f_p(Qn + 0.5 * dt * k1q)
        
        k3q = f_q(Pn + 0.5 * dt * k2p)
        k3p = f_p(Qn + 0.5 * dt * k2q)
        
        k4q = f_q(Pn + dt * k3p)
        k4p = f_p(Qn + dt * k3q)

        Qn = Qn + (1/6)*dt*(k1q + 2*k2q + 2*k3q + k4q)
        Pn = Pn + (1/6)*dt*(k1p + 2*k2p + 2*k3p + k4p)
    return Qn, Pn

def corretor (Qn, Pn, E0):

    E = 0.5 * Pn**2 - np.cos(Qn) + 1
    
    dE_dQ = np.sin(Qn)
    dE_dP = Pn
    grad2E = dE_dQ**2 + dE_dP**2

    # alpha = np.zeros_like(E)
    # for a in range(E.shape[0]):
    #     for b in range(E.shape[1]):
    #         if abs(E[a,b] - E0[a,b]) > 1e-8:
    #             alpha[a,b] = (E0[a,b] - E[a,b]) / grad2E[a,b]

    alpha = (E0 - E) / grad2E
        
    Qn = Qn + dE_dQ * alpha
    Pn = Pn + dE_dP * alpha

    return Qn, Pn

def plotar_imagem_pendulo (ax, metodo, dt, arr, cx:float, cy:float, r:float, tfs:list):
    h, w, _ = arr.shape

    qx = np.linspace(cx - r, cx + r, w)
    py = np.linspace(cy - r, cy + r, h)
    Q, P = np.meshgrid(qx, py)
    E0 = 0.5 * P**2 - np.cos(Q) + 1

    for tf in tfs:
        ax = plotar_transformacao(ax, dt, tf, Q, P, arr, metodo, E0)
    return ax

def plotar_imagens_pendulo (ax, metodo, dt, arr):
    h, w, _ = arr.shape
    
    # Esquerda
    center_x, center_y = 0, 1.8
    radius = 1.0

    qx = np.linspace(center_x - radius, center_x + radius, w)
    py = np.linspace(center_y - radius, center_y + radius, h)
    Q, P = np.meshgrid(qx, py)
    E0 = 0.5 * P**2 - np.cos(Q) + 1

    ax = plotar_transformacao(ax, dt, 3.0, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 2.0, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 1.0, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 0.0, Q, P, arr, metodo, E0)

    # Direita
    center_x, center_y = 2*np.pi, 1.0
    radius = 0.7

    qx = np.linspace(center_x - radius, center_x + radius, w)
    py = np.linspace(center_y - radius, center_y + radius, h)
    Q, P = np.meshgrid(qx, py)
    E0 = 0.5 * P**2 - np.cos(Q) + 1

    ax = plotar_transformacao(ax, dt, 5.0, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 3.7, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 2.5, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 1.2, Q, P, arr, metodo, E0)
    ax = plotar_transformacao(ax, dt, 0.0, Q, P, arr, metodo, E0)

    return ax

"""
SEPARADO
"""
# dt = 0.8
# titulo = r"Euler Simplético, $dt = {}$".format(dt)
# metodo = euler_simpletico
# arquivo = "euler_simpletico"

# # Plotando o campo
# fig, ax = plt.subplots(1,1)
# ax = plotar_campo(ax)

# # Plotando as imagens
# plotar_imagens_pendulo(ax, metodo, dt)

# ax.set_title(titulo)
# plt.tight_layout()
# plt.savefig(arquivo + ".png")
# plt.show()

"""
TODOS JUNTOS
"""