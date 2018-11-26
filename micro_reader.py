#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import matplotlib
matplotlib.use('Agg')
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



def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


list_devices = None
device = None
window = 200
channels = [1, 2]
downsample = 1
samplerate =  48000
interval = 30
batch = 33262

if any(c < 1 for c in channels):
    pass
#     parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in channels]  # Channel numbers start with 1
q = queue.Queue()
source_signal = np.zeros((len(channels), batch))
cur_size = 0


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::downsample, mapping])


def update_plot():
    global cur_size
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            continue
        #print("hello_up")
        shift = len(data)
        # print(data[::10])

        r_b = cur_size + data.shape[0]
        print(r_b)
        if r_b > batch:
            source_signal[:, cur_size:batch] = data.T[:, :batch - cur_size]
            # print(source_signal)
            test(source_signal)
            cur_size = 0
        else:
            source_signal[:, cur_size:r_b] = data.T
            cur_size = r_b


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
    R = pra.circular_2D_array(room_dim / 2, len(channels), 0., 0.15)
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



# def callback(indata, outdata, frames, time, status):
#     print("hello")
#     if status:
#         print(status)
#     outdata[:] = indata
#     print(indata)


try:

    if list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        samplerate = device_info['default_samplerate']

    length = int(window * samplerate / (1000 * downsample))
    plotdata = np.zeros((length, len(channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(channels) > 1:
        ax.legend(['channel {}'.format(c) for c in channels],
                  loc='lower left', ncol=len(channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom='off', top='off', labelbottom='off',
                   right='off', left='off', labelleft='off')
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=device, channels=max(channels),
        samplerate=samplerate, callback=audio_callback)
    #ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    threading.Thread(target=update_plot).start()
    with stream:
        sd.sleep(int(10 * 1000))


    #with sd.Stream(device=args.device, channels=max(args.channels),
     #   samplerate=args.samplerate, callback=callback):
      #  sd.sleep(int(10 * 1000))

except Exception as e:
    pass
    # parser.exit(type(e).__name__ + ': ' + str(e))