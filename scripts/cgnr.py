import numpy as np


def cgnr(g: np.ndarray, H: np.ndarray) -> np.ndarray:
    f = np.zeros(H.shape[1])
    r = g - H @ f
    z = H.T @ r
    p = z.copy()

    for _ in range(g.size):
        w = H @ p
        z_norm = np.linalg.norm(z) ** 2
        alpha = z_norm / (np.linalg.norm(w) ** 2)

        f = f + alpha * p
        error = np.linalg.norm(r)

        r = r - alpha * w
        error -= np.linalg.norm(r)

        if error < 1e-4:
            break

        z = H.T @ r
        beta = (np.linalg.norm(z) ** 2) / z_norm
        p = z + beta * p

    return f


h = np.loadtxt('../Dados/H-1.csv', delimiter=',')
g = np.loadtxt('../Dados/G-1.csv', delimiter=',')
# g = np.loadtxt('../Dados/G-2.csv', delimiter=',')

f = cgnr(g, h)
np.savetxt('output_f2.csv', f, delimiter=';')

print("Output saved")
