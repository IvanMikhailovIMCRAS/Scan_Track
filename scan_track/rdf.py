import time

import numpy as np

from .periodic_box import Box
from .scan_track import ReadTrack


class Atom:
    def __init__(self, x: float, y: float, z: float, btype: int):
        self.x = x
        self.y = y
        self.z = z
        self.btype = btype

    def get_distance(self, atom, box: Box):
        dx = atom.x - self.x
        dy = atom.y - self.y
        dz = atom.z - self.z
        (dx, dy, dz) = box.periodic_correct(dx, dy, dz)
        return np.sqrt(dx**2 + dy**2 + dz**2)


def rdf(
    group_A: np.ndarray, group_B: np.ndarray, box: Box, dr: float = 0.1
) -> np.array:
    min_box = min([box.x, box.y, box.z])
    g = np.zeros(int(2 * min_box / dr) + 1)
    v = np.zeros(int(2 * min_box / dr) + 1)
    for j in range(len(v)):
        v[j] = (4 / 3) * np.pi * (((j + 1) * dr) ** 3 - (j * dr) ** 3)
    for i, atm1 in enumerate(group_A):
        print(i)
        for atm2 in group_B:
            dx = atm1[0] - atm2[0]
            dy = atm1[1] - atm2[1]
            dz = atm1[2] - atm2[2]
            (dx, dy, dz) = box.periodic_correct(dx, dy, dz)
            dist = np.sqrt(dx**2 + dy**2 + dz**2)
            g[int(dist / dr)] += 1
    return g / v


def rdf_new(RT: ReadTrack, type_1: int, type_2: int, dr: float = 0.1) -> np.ndarray:
    # n_1 = list(RT.btype).count(type_1)
    # n_2 = list(RT.btype).count(type_2)
    rdf = np.zeros(int(RT.box.x / dr))
    for i in range(RT.num_atoms - 1):
        for j in range(i + 1, RT.num_atoms):
            if (RT.btype[i] == type_1 and RT.btype[j] == type_2) or (
                RT.btype[i] == type_2 and RT.btype[j] == type_1
            ):
                dx = RT.x[i] - RT.x[j]
                dy = RT.y[i] - RT.y[j]
                dz = RT.z[i] - RT.z[j]
                (dx, dy, dz) = RT.box.periodic_correct(dx, dy, dz)
                r = np.sqrt(dx**2 + dy**2 + dz**2)
                rdf[int(r / dr)] += 1
    return rdf


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    dr = 0.1
    RT = ReadTrack("/home/imc24/Serafim/Constructor/OU/")
    RT.one_step()
    rdf = rdf_new(RT=RT, type_1=1, type_2=2)
    count = 1
    v = np.zeros(len(rdf))
    for j in range(len(rdf)):
        v[j] = (4 / 3) * np.pi * (((j + 1) * dr) ** 3 - (j * dr) ** 3)

    while RT.one_step():
        time_start = time.time()
        print(count)
        rdf += rdf_new(RT=RT, type_1=1, type_2=2)
        count += 1
        time_end = time.time()
        print(f"time is:{time_end - time_start}sec.")

    n_1 = list(RT.btype).count(1)
    rdf = rdf / np.sum(rdf) * n_1
    rdf = rdf / v
    x = np.arange(len(rdf)) * dr
    plt.plot(x[: len(x) // 2], rdf[: len(rdf) // 2])
    plt.savefig("rdf_func2.png")

    # label = True
    # while RT.one_step():
    #     if label:
    #         N_A = 0
    #         N_B = 0
    #         for i in RT.btype:
    #             if i == 2:
    #                 N_A += 1
    #             elif i == 3:
    #                 N_B += 1
    #         group_A = np.zeros(shape = (N_A, 3))
    #         group_B = np.zeros(shape = (N_B, 3))
    #     label = False
    #     it = 0
    #     ik = 0
    #     for i in range(RT.num_atoms):
    #         if RT.btype[i] == 2:
    #             group_A[it] = [RT.x[i], RT.y[i], RT.z[i]]
    #             it += 1
    #         elif RT.btype[i] == 3:
    #             group_B[ik] = [RT.x[i], RT.y[i], RT.z[i]]
    #             ik += 1
    #     print(RT.time_step)
    # plt.plot(rdf(group_A, group_B, RT.box))
    # plt.show()
    # plt.close()

    # plt.xlim(0, RT.box.x/2 / 0.1)
    # plt.ylim(0, 2)
    # plt.plot(rdf(group_B, group_B, RT.box) / 3000)
    # plt.show()
