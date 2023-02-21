from scan_track import *
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    path = 'trajectory_sample'
    track = ReadTrack(path)
    bonds = read_bonds(path)
    R2 = []
    t = []
    os.system(command='rm *.ent')
    while track.one_step():
        dx = track.x[0]- track.x[-1]
        dy = track.y[0]- track.y[-1]
        dz = track.z[0]- track.z[-1]
        dx, dy, dz = track.box.periodic_correct(dx, dy, dz)
        R2.append(dx**2 + dy**2 + dz**2)
        t.append(track.time_step)

    R2 = np.array(R2)
    print('R2_mean: ', R2.mean())
    print('R2_std: ', R2.std())
    R2 -= R2.mean()
    t = np.array(t)
    
    plt.figure(figsize=(20,5))
    plt.plot(t, R2)
    plt.show()
    #plt.close()
    N = len(R2)
    Nt = N // 50
    autocor = np.correlate(R2, R2, mode='full')
    autocor = autocor[N:N+Nt]/autocor[N]
    tau = 0.0
    for i, ct in enumerate(autocor):
        if ct < np.exp(-1.):
            a = (autocor[i] - autocor[i-1]) / (t[i] - t[i-1])
            b = autocor[i] - a * t[i]
            tau = (np.exp(-1.) - b) / a
            print(t[i])
            break
    print('tau: ', tau)
    plt.figure(figsize=(20,5))
    plt.plot(autocor)
    plt.show()