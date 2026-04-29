# filename: codebase/step_6.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.rcParams['text.usetex'] = False
def main():
    data_dir = 'data/'
    boundaries_filepath = os.path.join(data_dir, 'phase_boundaries.csv')
    df_boundaries = pd.read_csv(boundaries_filepath)
    N_s = df_boundaries['N_s']
    H_species = df_boundaries['H_species_cutoff']
    H_Ne_30 = df_boundaries['H_Ne_30']
    H_Ne_60 = df_boundaries['H_Ne_60']
    H_Ne_100 = df_boundaries['H_Ne_100']
    H_dyn_sel_1 = 1.0 / N_s
    H_dyn_sel_05 = N_s**(-2.0/3.0)
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    ax1.plot(N_s, H_species, 'k-', linewidth=2, label='Species Cutoff (N_s <= M_Pl^2/H^2)')
    ax1.plot(N_s, H_Ne_60, 'r--', linewidth=2, label='e-fold Requirement (N_e=60)')
    ax1.plot(N_s, H_Ne_30, 'r:', linewidth=1.5, label='e-fold Requirement (N_e=30)')
    ax1.plot(N_s, H_Ne_100, 'r-.', linewidth=1.5, label='e-fold Requirement (N_e=100)')
    ax1.plot(N_s, H_dyn_sel_1, 'b-', linewidth=2, label='Dynamical Selection (F(x)=x)')
    ax1.plot(N_s, H_dyn_sel_05, 'b--', linewidth=2, label='Dynamical Selection (F(x)=x^0.5)')
    ax1.fill_between(N_s, H_species, 1, color='gray', alpha=0.3, label='Forbidden (Species Cutoff)')
    ax1.fill_between(N_s, H_Ne_60, H_species, color='red', alpha=0.1, label='Forbidden (N_e < 60)')
    ax1.axvline(1e2, color='g', linestyle='--', alpha=0.7, label='SM-like (N_s=10^2)')
    ax1.axvline(1e3, color='m', linestyle='--', alpha=0.7, label='MSSM-like (N_s=10^3)')
    ax1.axvspan(1e4, 1e6, color='y', alpha=0.2, label='GUT/String (N_s=10^4-10^6)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(1, 1e8)
    ax1.set_ylim(1e-8, 1e-1)
    ax1.set_xlabel('Number of Species N_s', fontsize=14)
    ax1.set_ylabel('Hubble Parameter H/M_Pl', fontsize=14)
    ax1.set_title('Phase Diagram: Constraints on Inflationary Parameter Space', fontsize=16)
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(loc='lower left', fontsize=10)
    plt.tight_layout()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plot1_filename = 'phase_diagram_1_' + timestamp + '.png'
    plot1_filepath = os.path.join(data_dir, plot1_filename)
    fig1.savefig(plot1_filepath, dpi=300)
    print('Phase diagram saved to ' + plot1_filepath)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    grid_filepath = os.path.join(data_dir, 'r_tensor_scalar_grid.npz')
    grid_data = np.load(grid_filepath)
    N_s_grid = grid_data['N_s']
    H_grid = grid_data['H']
    r_grid = grid_data['r']
    N_s_vals_grid = N_s_grid[0, :]
    H_vals_grid = H_grid[:, 0]
    Ns_plot_vals = [10**2, 10**4, 10**6]
    colors = ['g', 'y', 'c']
    for i in range(len(Ns_plot_vals)):
        Ns_val = Ns_plot_vals[i]
        color = colors[i]
        idx = np.argmin(np.abs(N_s_vals_grid - Ns_val))
        r_vals = r_grid[:, idx]
        label_str = 'N_s = 10^' + str(int(np.log10(Ns_val)))
        ax2.plot(H_vals_grid, r_vals, color=color, linewidth=2, label=label_str)
    ax2.axhline(0.036, color='r', linestyle='--', linewidth=2, label='Observational Bound (r < 0.036)')
    ax2.fill_between(H_vals_grid, 0.036, 1e2, color='red', alpha=0.1, label='Observationally Forbidden')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlim(1e-6, 1e-1)
    ax2.set_ylim(1e-25, 1e2)
    ax2.set_xlabel('Hubble Parameter H/M_Pl', fontsize=14)
    ax2.set_ylabel('Tensor-to-Scalar Ratio r', fontsize=14)
    ax2.set_title('Tensor-to-Scalar Ratio vs Hubble Scale', fontsize=16)
    ax2.grid(True, which="both", ls="--", alpha=0.5)
    ax2.legend(loc='upper left', fontsize=12)
    plt.tight_layout()
    plot2_filename = 'tensor_to_scalar_ratio_2_' + timestamp + '.png'
    plot2_filepath = os.path.join(data_dir, plot2_filename)
    fig2.savefig(plot2_filepath, dpi=300)
    print('Tensor-to-scalar ratio plot saved to ' + plot2_filepath)
    print('\n=== Key Statistics ===')
    print('Phase Diagram Boundaries at N_s = 100:')
    print('  Species Cutoff H/M_Pl: ' + str(1.0/np.sqrt(100)))
    print('  N_e=60 Cutoff H/M_Pl: ' + str(1.0/np.sqrt(60*100)))
    print('  Dynamical Selection (F(x)=x) H/M_Pl: ' + str(1.0/100))
    print('  Dynamical Selection (F(x)=x^0.5) H/M_Pl: ' + str(100**(-2.0/3.0)))
    print('\nObservational Bounds on H/M_Pl from r < 0.036:')
    for Ns_val in Ns_plot_vals:
        H_max = (0.036 / (3.2 * Ns_val))**(1.0/5.0)
        print('  For N_s = ' + str(Ns_val) + ', max allowed H/M_Pl: ' + str(H_max))
if __name__ == '__main__':
    main()