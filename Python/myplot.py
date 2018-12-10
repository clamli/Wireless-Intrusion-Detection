import matplotlib.pyplot as plt

def plot(data):
    fig, axs = plt.subplots(8, 1)
    x = range(data.shape[1])
    cnt = 0
    for channel in data:
        axs[cnt].set_title('channel '+ str(cnt+1))
        axs[cnt].plot(x, channel)
        cnt += 1
    plt.show()


# x = range(5)
# fig = plt.figure()
# ax = plt.axes()
# ax.plot(x, np.sin(x))
# plt.show()
