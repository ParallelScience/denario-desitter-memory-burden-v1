# filename: codebase/step_5.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def load_and_plot_synthesis(data_dir):
    plt.rcParams['text.usetex'] = False
    selection_data = np.load(os.path.join(data_dir, 'selection_data.npz'))
    H_sel = selection_data['H_vals']
    Ns_const = selection_data['Ns_const']
    Ns_log = selection_data['Ns_log']
    Ns_pow_05 = selection_data['Ns_pow_05']
    Ns_pow_1 = selection_data['Ns_pow_1']
    Ns_pow_2 = selection_data['Ns_pow_2']
    sim_data = np.load(os.path.join(data_dir, 'simulation_data.npz'))
    N_s_sim = sim_data['N_s_vals']
    H_sim = sim_data['H_vals']
    N_e_matrix = sim_data['N_e_matrix']
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    H_obs_min = 1e-5
    H_obs_max = 1e-4
    ax1 = axes[0]
    H_grid = np.logspace(-6, -1, 500)
    Ns_cutoff = 1.0 / H_grid**2
    Ns_efold = 1.0 / (60.0 * H_grid**2)
    ax1.plot(H_grid, Ns_cutoff, 'r-', lw=2, label='Species Cutoff (N_s = 1/H^2)')
    ax1.plot(H_grid, Ns_efold, 'b--', lw=2, label='e-fold Constraint (N_e=60)')
    ax1.fill_between(H_grid, Ns_cutoff, 1e15, color='red', alpha=0.2, label='Forbidden (Cutoff)')
    ax1.fill_between(H_grid, Ns_efold, Ns_cutoff, color='blue', alpha=0.1, label='Forbidden (N_e < 60)')
    ax1.axvspan(H_obs_min, H_obs_max, color='green', alpha=0.2, label='CMB Band')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(1e-6, 1e-1)
    ax1.set_ylim(1e0, 1e13)
    ax1.set_xlabel('Hubble Scale H / M_Pl')
    ax1.set_ylabel('Number of Species N_s')
    ax1.set_title('(a) Constraints Phase Diagram')
    ax1.grid(True, which='both', ls='--', alpha=0.5)
    ax1.legend(fontsize=9, loc='upper right')
    ax2 = axes[1]
    H_mesh, Ns_mesh = np.meshgrid(H_sim, N_s_sim)
    N_e_plot = np.clip(N_e_matrix, 1e-2, None)
    c = ax2.pcolormesh(H_mesh, Ns_mesh, N_e_plot, shading='auto', cmap='viridis', norm=mcolors.LogNorm(vmin=1, vmax=1e5))
    fig.colorbar(c, ax=ax2, label='Number of e-folds N_e')
    ax2.plot(H_grid, Ns_cutoff, 'r-', lw=1.5)
    ax2.plot(H_grid, Ns_efold, 'b--', lw=1.5)
    ax2.axvspan(H_obs_min, H_obs_max, color='green', alpha=0.2)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlim(1e-5, 1e-2)
    ax2.set_ylim(1e0, 1e8)
    ax2.set_xlabel('Hubble Scale H / M_Pl')
    ax2.set_ylabel('Number of Species N_s')
    ax2.set_title('(b) Stability Corridor (N_e Heatmap)')
    ax2.grid(True, which='both', ls='--', alpha=0.5)
    ax3 = axes[2]
    ax3.plot(H_sel, Ns_const, label='F = 1', lw=2)
    ax3.plot(H_sel, Ns_log, label='F = ln(1/H)', lw=2)
    ax3.plot(H_sel, Ns_pow_05, label='F = (1/H)^0.5', lw=2)
    ax3.plot(H_sel, Ns_pow_1, label='F = 1/H', lw=2)
    ax3.plot(H_sel, Ns_pow_2, label='F = (1/H)^2', lw=2, linestyle='--')
    ax3.axvspan(H_obs_min, H_obs_max, color='green', alpha=0.2, label='CMB Band')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlim(1e-6, 1e-1)
    ax3.set_ylim(1e0, 1e13)
    ax3.set_xlabel('Hubble Scale H / M_Pl')
    ax3.set_ylabel('Number of Species N_s')
    ax3.set_title('(c) Dynamical Selection')
    ax3.grid(True, which='both', ls='--', alpha=0.5)
    ax3.legend(fontsize=9, loc='upper right')
    plt.tight_layout()
    timestamp = int(time.time())
    plot_filename = os.path.join(data_dir, 'synthesis_constraints_5_' + str(timestamp) + '.png')
    plt.savefig(plot_filename, dpi=300)
    print('Synthesis plot saved to ' + plot_filename)

def main():
    data_dir = 'data'
    load_and_plot_synthesis(data_dir)

if __name__ == '__main__':
    main()