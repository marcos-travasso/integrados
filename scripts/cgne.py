import numpy as np


def cgne(g: np.ndarray, H: np.ndarray) -> np.ndarray:
    f = np.zeros(H.shape[1])
    r = g - H @ f
    p = H.T @ r
    
    for _ in range(g.size):
        w = H @ p
        z_norm = np.linalg.norm(p) ** 2
        alpha = z_norm / (np.linalg.norm(w) ** 2)
        
        f = f + alpha * p
        r = r - alpha * w
        
        if np.linalg.norm(r) < 1e-4:
            break
        
        z_new = H.T @ r
        beta = (np.linalg.norm(z_new) ** 2) / z_norm
        p = z_new + beta * p
    
    return f

h = np.loadtxt('../Dados/H-1.csv', delimiter=',')
g = np.loadtxt('../Dados/G-1.csv', delimiter=',')

f = cgne(g, h)
np.savetxt('output_f2.csv', f, delimiter=';')

print("Output saved")