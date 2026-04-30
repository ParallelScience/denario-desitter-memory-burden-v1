# filename: codebase/step_6.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = 'data'
    filepath = os.path.join(data_dir, 'step_3_parameter_sweep.npz')
    data = np.load(filepath)
    Ns_grid = data['Ns_grid']
    H_grid = data['H_grid']
    mask_BBN = data['mask_BBN']
    mask_species = data['mask_species']
    mask_quantum_breaking = data['mask_quantum_breaking']
    mask_ns_planck = data['mask_ns_planck']
    mask_success = mask_BBN & mask_species & mask_quantum_breaking & mask_ns_planck
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.contourf(Ns_grid, H_grid, mask_success, levels=[0.5, 1.5], colors=['#2ca02c'], alpha=0.6)
    Ns_vals = Ns_grid[0, :]
    H_vals = H_grid[:, 0]
    H_species = 1.0 / np.sqrt(Ns_vals)
    H_qb = 1.0 / np.sqrt(60.0 * Ns_vals)
    ax.fill_between(Ns_vals, H_species, 1.0, color='red', alpha=0.15)
    ax.fill_between(Ns_vals, H_qb, H_species, color='magenta', alpha=0.15)
    ax.plot(Ns_vals, H_species, color='red', lw=2, label='Species Cutoff (N_s = M_Pl^2/H^2)')
    ax.plot(Ns_vals, H_qb, color='magenta', lw=2, label='Quantum Breaking (N_e N_s = M_Pl^2/H^2)')
    ns_grid = data['ns_grid']
    ax.contour(Ns_grid, H_grid, ns_grid, levels=[0.961, 0.969], colors='blue', linestyles='solid', linewidths=2)
    ax.plot([], [], color='blue', lw=2, label='Planck n_s band (0.961 - 0.969)')
    ax.plot(Ns_vals, 1.0 / np.sqrt(Ns_vals), color='black', linestyle=':', lw=2.5, label='Dyn. Sel. (Constant F)')
    H_vals_line = np.logspace(-5, -2, 500)
    Ns_log = 1.0 / (H_vals_line**2 * np.log(1.0 / H_vals_line))
    ax.plot(Ns_log, H_vals_line, color='black', linestyle='--', lw=2.5, label='Dyn. Sel. (Logarithmic F)')
    H_power = 1.0 / Ns_vals
    ax.plot(Ns_vals, H_power, color='black', linestyle='-.', lw=2.5, label='Dyn. Sel. (Linear F, p=1)')
    ax.text(1e6, 5e-3, 'Species Cutoff\nViolated', color='darkred', fontsize=12, ha='center', va='center', fontweight='bold')
    ax.text(1e6, 2.5e-4, 'Quantum Breaking\nToo Fast (N_e < 60)', color='darkmagenta', fontsize=12, ha='center', va='center', fontweight='bold')
    ax.text(2, 5e-3, 'BBN Constraint (T_rh > 10 MeV)\nsatisfied everywhere in this domain', color='black', fontsize=11, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    if np.any(mask_success):
        success_Ns = Ns_grid[mask_success]
        success_H = H_grid[mask_success]
        mean_log_Ns = np.mean(np.log10(success_Ns))
        mean_log_H = np.mean(np.log10(success_H))
        ax.text(10**mean_log_Ns, 10**mean_log_H, 'Success\nRegion', color='darkgreen', fontsize=12, ha='center', va='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1, 1e8)
    ax.set_ylim(1e-5, 1e-2)
    ax.set_xlabel('Number of Species N_s', fontsize=14)
    ax.set_ylabel('Hubble Parameter H / M_Pl', fontsize=14)
    ax.set_title('Unified Phase Diagram: Constraints on Graviton Condensate Inflation', fontsize=16)
    ax.grid(True, which='both', linestyle='--', alpha=0.4)
    ax.legend(loc='lower left', fontsize=11, framealpha=0.9)
    plt.tight_layout()
    timestamp = str(int(time.time()))
    filename = 'unified_phase_diagram_' + timestamp + '.png'
    filepath_out = os.path.join(data_dir, filename)
    plt.savefig(filepath_out, dpi=300)
    print('Plot saved to ' + filepath_out)
    print('\n--- Phase Diagram Statistics ---')
    print('Total grid points: ' + str(mask_success.size))
    print('Points in success region: ' + str(np.sum(mask_success)))
    print('Points satisfying species bound: ' + str(np.sum(mask_species)))
    print('Points satisfying quantum breaking bound: ' + str(np.sum(mask_quantum_breaking)))
    print('Points satisfying Planck ns: ' + str(np.sum(mask_ns_planck)))
    print('Points satisfying BBN: ' + str(np.sum(mask_BBN)))
    if np.any(mask_success):
        print('\n--- Success Region Boundaries ---')
        print('Ns range: [' + str(np.min(success_Ns)) + ', ' + str(np.max(success_Ns)) + ']')
        print('H/M_Pl range: [' + str(np.min(success_H)) + ', ' + str(np.max(success_H)) + ']')

if __name__ == '__main__':
    main()