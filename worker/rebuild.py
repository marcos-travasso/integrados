import numpy as np
import cv2


def algorithm(g: list[float], H_dir: str, model: str, image_id: str, dimension: int) -> str:
    H = np.loadtxt(f"./Data/{H_dir}.csv", delimiter=',')
    g = np.array(g, dtype=np.float64)

    assert not np.isnan(H).any(), "H contains NaN values"
    assert not np.isnan(g).any(), "g contains NaN values"

    if model == "cgnr":
        f = cgnr(g, H)
    elif model == "cgne":
        f = cgne(g, H)
    else:
        raise ValueError(f"Invalid model: {model}")

    image = f.reshape(dimension, dimension).T

    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    image = np.uint8(image)

    output_path = f"./Outputs/output_{image_id}.png"
    cv2.imwrite(output_path, image)

    return f'output_{image_id}.png'


def cgnr(g: np.ndarray, H: np.ndarray) -> np.ndarray:
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