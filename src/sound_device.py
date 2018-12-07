#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import queue
import threading
import sys
import numpy as np
import pyroomacoustics as pra
from pyroomacoustics.doa import circ_dist
import time


import numpy as np
import sounddevice as sd
import requests
from threading import Thread

class MyThread(Thread):
    def __init__(self, url, data):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.url = url
        self.data = data
 
    def run(self):
        response = requests.post(self.url, json=self.data)
        if response.ok:
            # print(response.json()) #--> {'temp_1': 100, 'temp_2': 150}
            print(self.getName())
cnt = 0
cur_size = 0
batch = 33262
source_signal = np.zeros((8, batch))



def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=1, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    'channels', type=int, default=[1,2,3,4,5,6,7,8], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
args = parser.parse_args()
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    global cnt
    #print('hellocb')
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    #sd.sleep(100)
    raw_list = indata[::args.downsample, mapping].tolist()
    print(indata.shape)
    print(len(raw_list))
    data_from_pi = {'data' : raw_list}
    #data_from_pi = {'data' : 'hello'}
    '''thread = MyThread('http://192.168.1.144:5000/pi', data_from_pi)
    thread.setName(cnt)
    thread.start()
    thread.join()
    cnt += 1'''
    
    response = requests.post('http://192.168.1.144:5000/pi', json=data_from_pi)
    if response.ok:
        pass
        # print(response.json()) #--> {'temp_1': 100, 'temp_2': 150}
        #print('1')
    #q.put(indata[::args.downsample, mapping])

def test(source_signal):
    ######
    # We define a meaningful distance measure on the circle

    # Location of original source
    azimuth = 61. / 180. * np.pi  # 60 degrees
    distance = 3.  # 3 meters

    #######################
    # algorithms parameters
    SNR = 0.  # signal-to-noise ratio
    c = 343.  # speed of sound
    fs = 16000  # sampling frequency
    nfft = 256  # FFT size
    freq_bins = np.arange(5, 60)  # FFT bins to use for estimation

    # compute the noise variance
    sigma2 = 10 ** (-SNR / 10) / (4. * np.pi * distance) ** 2

    # Create an anechoic room
    room_dim = np.r_[10., 10.]
    aroom = pra.ShoeBox(room_dim, fs=fs, max_order=0, sigma2_awgn=sigma2)

    # add the source
    # source_location = room_dim / 2 + distance * np.r_[np.cos(azimuth), np.sin(azimuth)]
    # source_signal = np.random.randn((nfft // 2 + 1) * nfft)
    # aroom.add_source(source_location, signal=source_signal)

    # We use a circular array with radius 15 cm # and 12 microphones
    R = pra.circular_2D_array(room_dim / 2, 8, 0., 0.15)
    aroom.add_microphone_array(pra.MicrophoneArray(R, fs=aroom.fs))

    # run the simulation
    # aroom.simulate()
    # print(aroom.mic_array.signals)
    # print(source_signal)

    ################################
    # Compute the STFT frames needed
    X = np.array([
        pra.stft(signal, nfft, nfft // 2, transform=np.fft.rfft).T
        for signal in source_signal])

    ##############################################
    # Now we can test all the algorithms available
    algo_names = sorted(pra.doa.algorithms.keys())

    for algo_name in algo_names:
        # Construct the new DOA object
        # the max_four parameter is necessary for FRIDA only
        doa = pra.doa.algorithms[algo_name](R, fs, nfft, c=c, max_four=4)

        # this call here perform localization on the frames in X
        doa.locate_sources(X, freq_bins=freq_bins)

        doa.polar_plt_dirac()
        plt.title(algo_name)

        # doa.azimuth_recon contains the reconstructed location of the source
        print(algo_name)
        print('  Recovered azimuth:', doa.azimuth_recon / np.pi * 180., 'degrees')
        print('  Error:', circ_dist(azimuth, doa.azimuth_recon) / np.pi * 180., 'degrees')
        plt.savefig('./figures/fig'+str(time.time())+'.png')
        break

    # plt.show()


try:

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend(['channel {}'.format(c) for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom='off', top='off', labelbottom='off',
                   right='off', left='off', labelleft='off')
    fig.tight_layout(pad=0)
    print(args.device)
    print(args.samplerate)
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    #ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    #threading.Thread(target=update_plot).start()
    with stream:
        sd.sleep(int(10 * 1000))

    #with sd.Stream(device=args.device, channels=max(args.channels),
     #   samplerate=args.samplerate, callback=callback):
      #  sd.sleep(int(10 * 1000))

except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))