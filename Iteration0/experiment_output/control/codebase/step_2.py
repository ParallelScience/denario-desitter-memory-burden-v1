# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import matplotlib.pyplot as plt
import numpy as np
import os
import time

plt.rcParams['text.usetex'] = False

def plot_dynamical_system():
    data_dir = 'data/'
    filepath = os.path.join(data_dir, 'graviton_condensate_sim.npz')
    if not os.path.exists(filepath):
        print('Error: Data file not found at ' + filepath)
        return
    data = np.load(filepath)
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[1, 0:2])
    ax5 = fig.add_subplot(gs[1, 2])
    gamma_plot = 1.0
    Ns_list = [10, 100, 1000]
    colors = ['b', 'g', 'r']
    N_min = np.inf
    N_max = -np.inf
    print('Metastable Quasi-de Sitter Phase Plateau Values (gamma = ' + str(gamma_plot) + '):')
    for Ns, color in zip(Ns_list, colors):
        key_base = 'gamma_' + str(gamma_plot) + '_Ns_' + str(Ns)
        if key_base + '_t' not in data:
            continue
        t = data[key_base + '_t']
        N = data[key_base + '_N']
        Q = data[key_base + '_Q']
        H = data[key_base + '_H']
        Q_N = Q / N
        ax1.plot(t, H, label='N_s = ' + str(Ns), color=color)
        ax2.plot(t, N, label='N_s = ' + str(Ns), color=color)
        ax3.plot(t, Q_N, label='N_s = ' + str(Ns), color=color)
        ax4.plot(N, Q_N, label='Trajectory N_s = ' + str(Ns), color=color)
        N_min = min(N_min, np.min(N))
        N_max = max(N_max, np.max(N))
        dN_dt = -1.0 / np.sqrt(N) + gamma_plot * Q / (N**2)
        idx_min = np.argmin(np.abs(dN_dt))
        N_plateau = N[idx_min]
        H_plateau = H[idx_min]
        Q_N_plateau = Q_N[idx_min]
        print('  For N_s = ' + str(Ns) + ': N_plateau = ' + str(N_plateau) + ', H_plateau = ' + str(H_plateau) + ' M_Pl, Q_mem/N = ' + str(Q_N_plateau))
    if N_min < N_max:
        N_vals = np.logspace(np.log10(max(1e-5, N_min)), np.log10(N_max), 500)
        Q_N_null = np.sqrt(N_vals) / gamma_plot
        ax4.plot(N_vals, Q_N_null, 'k--', linewidth=2, label='dN/dt = 0 Nullcline')
    ax1.set_xlabel('Time t (M_Pl^-1)')
    ax1.set_ylabel('Hubble parameter H (M_Pl)')
    ax1.set_title('Evolution of Hubble Parameter')
    ax1.set_yscale('log')
    ax1.grid(True, which='both', ls='--', alpha=0.5)
    ax1.legend()
    ax2.set_xlabel('Time t (M_Pl^-1)')
    ax2.set_ylabel('Occupation Number N (M_Pl^2)')
    ax2.set_title('Evolution of Occupation Number')
    ax2.set_yscale('log')
    ax2.grid(True, which='both', ls='--', alpha=0.5)
    ax2.legend()
    ax3.set_xlabel('Time t (M_Pl^-1)')
    ax3.set_ylabel('Memory Load Ratio Q_mem/N (dimensionless)')
    ax3.set_title('Evolution of Memory Load Ratio')
    ax3.set_yscale('log')
    ax3.grid(True, which='both', ls='--', alpha=0.5)
    ax3.legend()
    ax4.set_xlabel('Occupation Number N (M_Pl^2)')
    ax4.set_ylabel('Memory Load Ratio Q_mem/N (dimensionless)')
    ax4.set_title('Phase Portrait: Attractor Dynamics (gamma = 1.0)')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.grid(True, which='both', ls='--', alpha=0.5)
    ax4.legend()
    H_vals = np.logspace(-6, -2, 200)
    Ne = 60
    Ns_qb = [10**2, 10**4, 10**6]
    colors_qb = ['c', 'm', 'y']
    print('\nQuantum Breaking Thresholds (H where t_life / t_qb = 1 for N_e = 60):')
    for Ns, color in zip(Ns_qb, colors_qb):
        ratio = Ne * Ns * (H_vals**2)
        ax5.plot(H_vals, ratio, label='N_s = ' + str(Ns), color=color, linewidth=2)
        H_threshold = 1.0 / np.sqrt(Ne * Ns)
        print('  For N_s = ' + str(Ns) + ', H_threshold = ' + str(H_threshold) + ' M_Pl')
    ax5.axhline(1.0, color='k', linestyle='--', linewidth=2, label='Breaking Threshold (Ratio=1)')
    ax5.set_xlabel('Hubble parameter H (M_Pl)')
    ax5.set_ylabel('Ratio t_life / t_qb (dimensionless)')
    ax5.set_title('Quantum Breaking Ratio (N_e = 60)')
    ax5.set_xscale('log')
    ax5.set_yscale('log')
    ax5.grid(True, which='both', ls='--', alpha=0.5)
    ax5.legend()
    fig.tight_layout()
    timestamp = int(time.time())
    plot_filename = 'dynamical_system_plot_2_' + str(timestamp) + '.png'
    plot_filepath = os.path.join(data_dir, plot_filename)
    fig.savefig(plot_filepath, dpi=300)
    print('\nDynamical system plot saved to ' + plot_filepath)

if __name__ == '__main__':
    plot_dynamical_system()