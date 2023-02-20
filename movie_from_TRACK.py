from scan_track import *

PALLET = 'NOCSPF'
 
def print_ent_file(track, bonds, filename):
    file = open(filename, 'w')    
    length_pallet = len(PALLET)
    for i in range(track.num_atoms):
        if 0 < track.btype[i] < length_pallet:
            symbol = PALLET[track.btype[i]-1]  
        else:
            symbol = 'X'
        line = f'HETATM{i+1:5d}  {symbol}{i+1:12d}{track.x[i]:12.3f}{track.y[i]:8.3f}{track.z[i]:8.3f}\n'
        file.write(line.format(i, symbol, track.x, track.y, track.z))  
    for b in bonds: 
        dx = abs(track.x[b[0]-1] - track.x[b[1]-1]) 
        dy = abs(track.y[b[0]-1] - track.y[b[1]-1]) 
        dz = abs(track.z[b[0]-1] - track.z[b[1]-1]) 
        if dx < track.box.x/2 and dy < track.box.y/2 and dz < track.box.z/2:  
            file.write(f'CONECT{b[0]:5d}{b[1]:5d}\n')
    file.close()       
        
if __name__ == '__main__':
    path = '/home/imc/Serafim/Triblock_relax_na_06/'
    track = ReadTrack(path)
    bonds = read_bonds(path)
    while track.one_step():
        print_ent_file(track, bonds, f'picture{track.time_step:012d}.ent')