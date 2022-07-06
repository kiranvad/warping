import numpy as np
from warping import compute_warping
import matplotlib.pyplot as plt


def gaussian(x, mu, sig):
    scale = 1/(np.sqrt(2*np.pi)*sig)
    return scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def plot(t, f1, f2, f2_gamma, gamma):
    fig, axs = plt.subplots(1,2, figsize=(2*4, 4))
    axs[0].plot(x, f1, label='Target')
    axs[0].plot(x, f2, color='k', label='Source')
    axs[0].plot(x, f2_gamma, color='k', ls='--', label='Warped')
    axs[0].legend()

    axs[1].plot(t, gamma, color='k', ls='--')
    axs[1].plot(t, t, color='k')
    axs[1].set_title('warping function')
    
    plt.show()  
    
x = np.linspace(-7, 7, num=200)
f1 = gaussian(x, -1.5, 1.0)
f2 = gaussian(x, 1.5, 1.5)

time = np.linspace(0,1, 200)

gamma, f2_gamma = compute_warping(time, f1, f2, lam=0.0, grid_dim=15)
plot(time, f1, f2, f2_gamma, gamma) 


