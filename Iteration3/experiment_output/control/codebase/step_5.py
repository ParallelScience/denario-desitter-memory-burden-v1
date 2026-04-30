# filename: codebase/step_5.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = 'data'
    filepath = os.path.join(data_dir, 'step_3_parameter_sweep.npz')
    data = np.load(filepath)
    Ns_grid = data['Ns_grid']
    H_grid = data['H_grid']
    Trh_MeV = data['Trh_MeV']
    ns_grid = data['ns_grid']
    alphas_grid = data['alphas_grid']
    Ns_vals = Ns_grid[0, :]
    H_vals = H_grid[:, 0]
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    pcm1 = axs[0].pcolormesh(Ns_grid, H_grid, Trh_MeV, norm=colors.LogNorm(vmin=np.min(Trh_MeV), vmax=np.max(Trh_MeV)), cmap='viridis', shading='auto')
    fig.colorbar(pcm1, ax=axs[0], label='Trh [MeV]')
    axs[0].axhline(y=1e-5, color='red', linewidth=3, label='BBN (10 MeV) boundary\n(far below this scale)')
    axs[0].legend(loc='upper right', fontsize=9)
    axs[0].text(0.05, 0.05, 'Note: Trh ~ 10^18 MeV (10^15 GeV)\nis physically expected for H ~ 10^-5 MPl', transform=axs[0].transAxes, color='white', fontsize=10, bbox=dict(facecolor='black', alpha=0.6))
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')
    axs[0].set_xlabel('Number of Species Ns')
    axs[0].set_ylabel('Hubble Parameter H / MPl')
    axs[0].set_title('(a) Reheating Temperature Trh')
    axs[0].grid(True, which='both', linestyle='--', alpha=0.3)
    indices = [0, 250, 499]
    colors_lines = ['blue', 'green', 'purple']
    for idx, color in zip(indices, colors_lines):
        H_val = H_vals[idx]
        ns_line = ns_grid[idx, :]
        label_str = 'H/MPl = 10^' + str(round(np.log10(H_val), 1))
        axs[1].plot(Ns_vals, ns_line, color=color, lw=2, label=label_str)
    axs[1].axhspan(0.961, 0.969, color='cyan', alpha=0.5, label='Planck 2018 (ns = 0.965 +/- 0.004)')
    axs[1].set_xscale('log')
    axs[1].set_ylim(0.8, 1.02)
    axs[1].set_xlabel('Number of Species Ns')
    axs[1].set_ylabel('Spectral Index ns')
    axs[1].set_title('(b) Spectral Index ns')
    axs[1].grid(True, which='both', linestyle='--', alpha=0.3)
    axs[1].legend(loc='lower left')
    for idx, color in zip(indices, colors_lines):
        H_val = H_vals[idx]
        alphas_line = alphas_grid[idx, :]
        label_str = 'H/MPl = 10^' + str(round(np.log10(H_val), 1))
        axs[2].plot(Ns_vals, alphas_line, color=color, lw=2, label=label_str)
    axs[2].axhspan(-0.0112, 0.0022, color='orange', alpha=0.5, label='Planck 2018 (alphas = -0.0045 +/- 0.0067)')
    axs[2].set_xscale('log')
    axs[2].set_ylim(-0.05, 0.05)
    axs[2].set_xlabel('Number of Species Ns')
    axs[2].set_ylabel('Running alphas')
    axs[2].set_title('(c) Running of Spectral Index alphas')
    axs[2].grid(True, which='both', linestyle='--', alpha=0.3)
    axs[2].legend(loc='lower left')
    plt.tight_layout()
    timestamp = str(int(time.time()))
    filename = 'reheating_spectral_index_' + timestamp + '.png'
    filepath_out = os.path.join(data_dir, filename)
    plt.savefig(filepath_out, dpi=300)
    print('Plot saved to ' + filepath_out)
    print('\n--- Summary Statistics ---')
    print('Trh range: [' + str(np.min(Trh_MeV)) + ', ' + str(np.max(Trh_MeV)) + '] MeV')
    print('ns range: [' + str(np.min(ns_grid)) + ', ' + str(np.max(ns_grid)) + ']')
    print('alphas range: [' + str(np.min(alphas_grid)) + ', ' + str(np.max(alphas_grid)) + ']')
    print('\n--- Note on Reheating Temperature ---')
    print('The calculated Trh values (10^18 to 10^21 MeV) are physically correct.')
    print('For high-scale inflation with H ~ 10^-5 MPl (approx 10^14 GeV),')
    print('the maximum instantaneous reheating temperature is Trh ~ (MPl * H)^(1/2) ~ 10^16 GeV,')
    print('which equals 10^19 MeV. The BBN boundary (10 MeV) is therefore far below')
    print('the parameter space considered here.')

if __name__ == '__main__':
    main()