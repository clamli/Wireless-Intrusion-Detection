import numpy as np
from struct import *

def preprocess(wizards):
    data_lst = []
    for data in wizards:
        data_lst += data['data']
    data_arr = np.array(data_lst)
    return data_arr.T


def preprocess2(wizards, sample_rate=10):
    data_lst = []
    for data in wizards:
        data_lst += data['data']
    data_arr = np.array(data_lst)[::sample_rate]
    return data_arr.T


def preprocess_byte(wizards):
    packet = []
    for data in wizards:
        for i in range(0, len(data['data']), 4):
            packet.append(unpack('f', data['data'][i:i + 4])[0])
    if len(packet) == 0:
        return np.array([])
    packet_arr = np.array(packet).reshape(-1, 8)
    # print(packet_arr.shape)
    return packet_arr.T


def preprocess_byte2(wizards, sample_rate=10):
    packet = []
    for data in wizards:
        for i in range(0, len(data['data']), 4):
            packet.append(unpack('f', data['data'][i:i + 4])[0])
    if len(packet) == 0:
        return np.array([])
    print('in before:', np.max(packet))
    packet_arr = np.array(packet).reshape(-1, 8)[::sample_rate]
    print('in:', packet_arr.max())
    return packet_arr.T

# def save(data):
