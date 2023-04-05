from scan_track import ReadTrack, read_bonds
import numpy as np
import matplotlib.pyplot as plt

def cosine(x1, y1, x2, y2):
    return (x1*x2 + y1*y2) / (x1**2 + y1**2)**0.5 / (x2**2 + y2**2)**0.5

def scroll(n):
    lst = list(range(n))
    for i in range(len(lst)):
        yield lst
        lst = [lst.pop()] + lst

track = ReadTrack("/home/imc/SEMISHIN/new_m=2/")
track.one_step()
n_dendron = 0
for i in range(1, len(track.btype)):
    if track.btype[i-1] == 1 and track.btype[i] == 2:
        n_dendron += 1
n_beads = list(track.btype).count(2) // n_dendron
print(n_beads)
cm_x = np.zeros(n_dendron)
cm_y = np.zeros(n_dendron)
corr = np.zeros(n_dendron)
n_step = 0
while track.one_step():
    n_step += 1
    x = np.zeros(n_beads*n_dendron)
    y = np.zeros(n_beads*n_dendron)
    z = np.zeros(n_beads*n_dendron)
    count = 0
    for i in range(0, len(track.btype)):
        if track.btype[i] == 2:
            x[count] = track.x[i]
            y[count] = track.y[i]
            z[count] = track.z[i]
            count += 1
    for d in range(n_dendron):
        cm_x[d] = np.sum(x[d*n_beads:(d+1)*n_beads]) / n_beads
        cm_y[d] = np.sum(y[d*n_beads:(d+1)*n_beads]) / n_beads
    sc = scroll(n_dendron)
    for d in sc:
        count = 0
        lst = list(d)
        for i in lst:
            corr[count] += cosine(cm_x[i], cm_y[i], cm_x[lst[0]], cm_y[lst[0]])
            count += 1
plt.plot(corr/n_step / n_dendron)
plt.show()