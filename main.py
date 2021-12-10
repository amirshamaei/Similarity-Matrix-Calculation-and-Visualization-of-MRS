# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import scipy.io as sio
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
t_step = 1/4000
global signal
def savefig(path):
    if True:
        plt.savefig(path + ".svg", format="svg")
        plt.savefig(path + " .png", format="png", dpi=800)
def ppm2p(r):
    r=4.7-r
    return ((123*r)/(1/(t_step*len(signal))))+len(signal)/2
#%%
def similarityMat(insignalt, name, r1, r2):
    p1 = int(ppm2p(r1))
    p2 = int(ppm2p(r2))
    insignal = np.fft.fftshift(np.fft.fft(np.conj(insignalt), axis=0))
    sMat = np.zeros((np.shape(insignal)[1], np.shape(insignal)[1]))
    for i in range(0, np.shape(insignal)[1]):
        for j in range(i, np.shape(insignal)[1]):
            # sMat[i][j] = np.mean(np.abs(insignal[p1:p2, i] - insignal[p1:p2, j]))
            sMat[i][j] = np.abs(np.real(np.vdot(insignal[p1:p2, i],insignal[p1:p2, j])))
            sMat[j][i] = sMat[i][j]
    sMat = sMat/np.max(sMat)
    cmap = sns.diverging_palette(0, 120, 90, 60, as_cmap=True)
    mask = np.triu(np.ones_like(sMat, dtype=np.bool))
    # adjust mask and df
    # mask = mask[1:, :-1]
    sns.heatmap(np.log(sMat), mask=mask, cmap=cmap)
    savefig(name + str(np.shape(insignal)[1]) + "_" + "similarity")
    plt.show()
    sum = np.sum(sMat)
    print(sum)
    filetxt = open(name + str(np.shape(insignal)[1]) + "_" + "similaritySum.txt", 'w')
    filetxt.write("--- %s sum ---" % (sum))
    return sMat
 # Press Ctrl+F8 to toggle the breakpoint.
def main():
    mat = sio.loadmat('CSI_Ana.mat')
    global signal
    signal = mat['data']
    signal = np.reshape(signal,(1024,-1,32))
    similarityMat(signal[:,5,:], "name", 4.5, 0)
    # reshape = np.reshape(signal[:,:,0],(1024,9,9))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


