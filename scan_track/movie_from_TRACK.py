from scan_track import *
import os

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
    path = 'trajectory_sample'
    track = ReadTrack(path)
    bonds = read_bonds(path)
    list_ent = list()
    os.system(command='rm *.ent')
    while track.one_step():
        line = f'picture_{track.time_step:012d}.ent'
        list_ent.append(line)
        print_ent_file(track, bonds, line)
    script_spt = open('script.spt', 'w')
    for name_ent in list_ent:
        script_spt.write(f'load FILES {name_ent};\n')
        script_spt.write('background white  ;\n')
        script_spt.write('set window 700 700; \n')
        script_spt.write('select oxygen;\n')
        script_spt.write('spacefill 0.0;\n')
        script_spt.write('wireframe 0.2;\n')
        script_spt.write('set scale3d 4.8;\n')
        script_spt.write('select nitrogen;\n')
        script_spt.write('spacefill 0.5; \n')
        script_spt.write(f'write JPG {name_ent[:-4]}.jpg;\n')
    script_spt.write('exitjmol\n')
    script_spt.close()
    os.system(command='rm *.jpg')
    os.system(command='java -jar /usr/share/java/Jmol.jar -s script.spt')
    os.system(command='rm *.ent')
    # os.system(command=r'ffmpeg -r 10 -i *.jpg -b 300000k  -y test.avi') # TO DO why is it not working
    os.system(command='convert -delay 10 *.jpg myimage.gif')
    os.system(command='rm *.jpg')
