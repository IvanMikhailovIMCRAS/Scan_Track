from typing import Dict

import numpy as np


class Latties:
    def __init__(self, n: int, box_size: float):
        self.n = n
        self.box_size = box_size
        lat = []
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    lat.append([i, j, k])
        lat.pop(0)
        self.lat = np.array(lat)
        wave_vector = set()
        for element in self.lat:
            wave_vector.add(np.sum(element**2))
        self.wave_vector = np.array(list(wave_vector))

    def structure_factor(self, x, y, z) -> Dict:
        assert len(x) == len(y) == len(z)
        prod = 0.0
        index = 0
        sf = dict.fromkeys(self.wave_vector, [])
        for k in self.lat:
            q = k * 2 * np.pi / self.box_size
            sk = 0
            sk_cos = 0
            sk_sin = 0
            for j in range(len(x)):
                prod = x[j] * q[0] + y[j] * q[1] + z[j] * q[2]
                sk_cos += np.cos(prod)
                sk_sin += np.sin(prod)
            sk = sk_cos**2 + sk_sin**2
            index = k[0] ** 2 + k[1] ** 2 + k[2] ** 2
            sf[index] = sf[index] + [sk]
        for s in sf:
            sf[s] = np.array(sf[s]).mean / len(x)
        return sf


if __name__ == "__main__":
    L = Latties(1, 3)
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    z = np.array([1, 2, 3])
    d = L.structure_factor(x, y, z)
