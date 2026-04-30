# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import os
import time

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = 'data'
    filepath = os.path.join(data_dir, 'step_2_time_series.npz')
    data = np.load(filepath)
    t_smooth = data['t_smooth']
    N_smooth = data['N_smooth']
    Q_smooth = data['Q_smooth']
    H_smooth = data['H_smooth']
    stoc_indices = []
    for key in data.keys():
        if key.startswith('t_stoc_'):
            stoc_indices.append(key.split('_')[-1])
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs[0, 0].plot(t_smooth, H_smooth, color='blue', lw=2)
    axs[0, 0].set_title('(a) Smooth Evolution of Hubble Parameter H(t)')
    axs[0, 0].set_xlabel('Time t [Planck units]')
    axs[0, 0].set_ylabel('H(t) [M_Pl]')
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)
    axs[0, 1].plot(t_smooth, Q_smooth, color='green', lw=2)
    axs[0, 1].set_title('(b) Smooth Evolution of Memory Load Q_mem(t)')
    axs[0, 1].set_xlabel('Time t [Planck units]')
    axs[0, 1].set_ylabel('Q_mem(t)')
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)
    for idx in stoc_indices:
        t_stoc = data['t_stoc_' + str(idx)]
        H_stoc = data['H_stoc_' + str(idx)]
        axs[1, 0].plot(t_stoc, H_stoc, lw=1.5, alpha=0.8, label='Realization ' + str(int(idx)+1))
    axs[1, 0].set_title('(c) Stochastic Evolution of H(t)')
    axs[1, 0].set_xlabel('Time t [Planck units]')
    axs[1, 0].set_ylabel('H(t) [M_Pl]')
    axs[1, 0].grid(True, linestyle='--', alpha=0.7)
    axs[1, 0].legend()
    gamma_val = 1e5
    N_min = np.min(N_smooth)
    N_max = np.max(N_smooth)
    for idx in stoc_indices:
        N_stoc = data['N_stoc_' + str(idx)]
        N_min = min(N_min, np.min(N_stoc))
        N_max = max(N_max, np.max(N_stoc))
    N_margin = (N_max - N_min) * 0.1
    if N_margin == 0:
        N_margin = N_min * 0.1
    N_vals = np.linspace(N_min - N_margin, N_max + N_margin, 500)
    Q_nullcline = (N_vals**(1.5)) / gamma_val
    axs[1, 1].plot(N_vals, Q_nullcline, 'k--', lw=2, label='Nullcline dN/dt = 0')
    axs[1, 1].plot(N_smooth, Q_smooth, color='red', lw=2, label='Smooth Trajectory')
    for idx in stoc_indices:
        N_stoc = data['N_stoc_' + str(idx)]
        Q_stoc = data['Q_stoc_' + str(idx)]
        axs[1, 1].plot(N_stoc, Q_stoc, lw=1, alpha=0.5)
    axs[1, 1].set_title('(d) Phase-Space Portrait (N, Q_mem)')
    axs[1, 1].set_xlabel('Graviton Number N')
    axs[1, 1].set_ylabel('Memory Load Q_mem')
    axs[1, 1].grid(True, linestyle='--', alpha=0.7)
    axs[1, 1].legend()
    plt.tight_layout()
    timestamp = str(int(time.time()))
    plot_filename = 'stability_stochastic_stress_test_' + timestamp + '.png'
    plot_filepath = os.path.join(data_dir, plot_filename)
    plt.savefig(plot_filepath, dpi=300)
    print('Plot saved to ' + plot_filepath)

if __name__ == '__main__':
    main()