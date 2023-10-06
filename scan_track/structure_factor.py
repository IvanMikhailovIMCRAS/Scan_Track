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
        self.lat = np.array(lat)
        wave_vector = set()
        for element in self.lat:
            wave_vector.add(np.sum(element**2))
        self.wave_vector = np.array(list(wave_vector))


if __name__ == "__main__":
    L = Latties(3, 3)
    print(L.wave_vector)
