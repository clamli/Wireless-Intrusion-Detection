import time
import sounddevice as sd

from Database import Database
import myutils
import myplot
import processor

_author_ = 'Boyi Li'

# N = 1
# database = Database("mongodb://192.168.1.144:27017")
# analyzed_id = []

class Controller:
    def __init__(self):
        self.ang_lo = 20
        self.ang_up = 40
        self.ene_thr = 130
        self.cos_thr = 0.9

    def predict(self, database, N=1):
        data = myutils.preprocess_byte(database.read_records(N))
        # if data.shape[0] != 0:

            # myplot.plot(data)
        # print('!!!!!!', data.shape[0])
        # if data.shape[0] != 0:
            # print(data[:, 0:6])
            # sd.play(data[1], 44100)
        print('controller:', data[1].max())
        angle = processor.doa(data)     # angle
        energy = processor.enec(data)   # energy
        avg_cos_sim = processor.enve_sim(data)  # cosine sim

        # print(data.shape)
        print(angle)
        print(energy)
        print(avg_cos_sim)
        if (angle >= self.ang_lo and angle <= self.ang_up) and (energy > self.ene_thr) and avg_cos_sim < self.cos_thr:
            return True, round(angle,2), round(energy,2), round(avg_cos_sim,2)
        else:
            return False, round(angle,2), round(energy,2), round(avg_cos_sim,2)






