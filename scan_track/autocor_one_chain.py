import matplotlib.pyplot as plt
import numpy as np

from .scan_track import *

if __name__ == "__main__":
    path = "trajectory_sample"
    track = ReadTrack(path)
    bonds = read_bonds(path)
    R2 = []
    t = []
    while track.one_step():
        x = 0.0
        y = 0.0
        z = 0.0
        for b in bonds:
            dx = track.x[b[1] - 1] - track.x[b[0] - 1]
            dy = track.y[b[1] - 1] - track.y[b[0] - 1]
            dz = track.z[b[1] - 1] - track.z[b[0] - 1]
            dx, dy, dz = track.box.periodic_correct(dx, dy, dz)
            x += dx
            y += dy
            z += dz
        R2.append(x**2 + y**2 + z**2)
        t.append(track.time_step)

    R2 = np.array(R2)
    print("R2_mean: ", R2.mean())
    print("R2_std: ", R2.std())
    R2 -= R2.mean()
    t = np.array(t)

    plt.figure(figsize=(20, 5))
    plt.plot(t, R2)
    plt.show()
    # plt.close()
    N = len(R2)
    Nt = N // 50
    autocor = np.correlate(R2, R2, mode="full")
    autocor = autocor[N : N + Nt] / autocor[N]
    tau = 0.0
    for i, ct in enumerate(autocor):
        if ct < np.exp(-1.0):
            a = (autocor[i] - autocor[i - 1]) / (t[i] - t[i - 1])
            b = autocor[i] - a * t[i]
            tau = (np.exp(-1.0) - b) / a
            print(t[i])
            break
    print("tau: ", tau)
    plt.figure(figsize=(20, 5))
    plt.plot(autocor)
    plt.show()
