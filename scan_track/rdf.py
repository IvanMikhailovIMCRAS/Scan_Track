from periodic_box import Box
import numpy as np
from typing import List, Tuple

class Atom():
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
    
        
def rdf(group_A: np.ndarray, group_B: np.ndarray, box: Box, dr: float = 0.1) -> np.array:
    min_box = min([box.x, box.y, box.z])
    g = np.zeros(int(2*min_box/dr) + 1)
    v = np.zeros(int(2*min_box/dr) + 1)
    for j in range(len(v)):
        v[j] = (4/3) * np.pi * (((j+1)*dr)**3 - (j*dr)**3)
    for i,atm1 in enumerate(group_A):
        print(i)
        for atm2 in group_B:
            dx = atm1[0] - atm2[0]
            dy = atm1[1] - atm2[1]
            dz = atm1[2] - atm2[2]
            (dx, dy, dz) = box.periodic_correct(dx, dy, dz)
            dist = np.sqrt(dx**2 + dy**2 + dz**2)
            g[int(dist/dr)] += 1
    return g / v
   
if __name__ == "__main__":
    from scan_track import ReadTrack
    import matplotlib.pyplot as plt
    RT = ReadTrack("/home/imc/SEMISHIN/first_helix/Rod_brush/")
    label = True
    while RT.one_step():
        if label:
            N_A = 0
            N_B = 0
            for i in RT.btype:
                if i == 2:
                    N_A += 1
                elif i == 3:
                    N_B += 1
            group_A = np.zeros(shape = (N_A, 3))
            group_B = np.zeros(shape = (N_B, 3))
        label = False
        it = 0
        ik = 0
        for i in range(RT.num_atoms):
            if RT.btype[i] == 2:
                group_A[it] = [RT.x[i], RT.y[i], RT.z[i]]
                it += 1
            elif RT.btype[i] == 3:
                group_B[ik] = [RT.x[i], RT.y[i], RT.z[i]]
                ik += 1
        print(RT.time_step)
    plt.plot(rdf(group_A, group_B, RT.box))
    plt.show()
    plt.close()
    
    plt.xlim(0, RT.box.x/2 / 0.1)
    plt.ylim(0, 2)
    plt.plot(rdf(group_B, group_B, RT.box) / 3000)
    plt.show()