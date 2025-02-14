import os

import numpy as np
import cv2


def algorithm(g: list[float], H_dir: str, model: str, image_id: str, dimension: int) -> (str, int):
    H = np.loadtxt(os.path.join(os.path.dirname(__file__), f"../worker/Data/{H_dir}.csv"), delimiter=',')
    g = np.array(g, dtype=np.float64)

    assert not np.isnan(H).any(), "H contains NaN values"
    assert not np.isnan(g).any(), "g contains NaN values"

    if model == "cgnr":
        f, it = cgnr(g, H)
    elif model == "cgne":
        f, it = cgne(g, H)
    else:
        raise ValueError(f"Invalid model: {model}")

    image = f.reshape(dimension, dimension).T

    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    image = np.uint8(image)

    output_path = os.path.dirname(__file__) + f"/Outputs/output_{image_id}.png"
    cv2.imwrite(output_path, image)

    return output_path, it


def cgnr(g: np.ndarray, H: np.ndarray) -> (np.ndarray, int):
    f = np.zeros(H.shape[1])
    r = g - H @ f
    p = H.T @ r

    i = 0
    for _ in range(g.size):
        i += 1
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

    return f, i


def cgne(g: np.ndarray, H: np.ndarray) -> (np.ndarray, int):
    f = np.zeros(H.shape[1])
    r = g - H @ f
    p = H.T @ r

    i = 0
    for _ in range(g.size):
        i += 1
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

    return f, i