import os
import numpy as np

def periodic(coord, box):
        if abs(coord) > 0.5 * box: 
            return coord - np.sign(coord) * box
        return coord 
    
class Box():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def periodic_correct(self, xb, yb, zb):
        xb = periodic(xb, self.x)
        yb = periodic(yb, self.y)
        zb = periodic(zb, self.z)
        return xb, yb, zb
    
class ReadTrack():
    def __init__(self, path=''):
        self.path = os.path.join(path, 'TRACK')
        self.time_step = 0
        try:
           self.file_track = open(self.path, 'r')
        except:
            raise FileNotFoundError(f'{str(self.path)} is not found')
        try:
            title = self.file_track.readline().split() 
            self.num_atoms = int(title[1])
            self.box = Box(float(title[3]), float(title[4]), float(title[5])) 
        except:
            self.file_track.close()
            raise FileNotFoundError(f'{str(self.path)} is not correct') 
        self.x = np.zeros(self.num_atoms, dtype=float) 
        self.y = np.zeros(self.num_atoms, dtype=float) 
        self.z = np.zeros(self.num_atoms, dtype=float) 
        self.btype = np.zeros(self.num_atoms, dtype=int)
        self.iterator = list(range(self.num_atoms))
          
    def one_step(self):
        try:
            title = self.file_track.readline().split()
            self.time_step = int(title[1])
            for i in self.iterator:
                record = self.file_track.readline().split()
                self.x[i] = float(record[1])
                self.y[i] = float(record[2])
                self.z[i] = float(record[3])
                self.btype[i] = int(record[4])                
            return True
        except:
            self.file_track.close()
            return False         
            
if __name__ == '__main__':
    RT = ReadTrack('/home/imc/Serafim/Triblock_relax_na_06/') 
    while RT.one_step():
        print(RT.time_step)
    