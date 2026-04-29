# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = False

def generate_phase_diagram():
    data_dir = "data/"
    filepath = os.path.join(data_dir, "constraint_boundaries.npz")
    if not os.path.exists(filepath):
        print("Error: Data file not found at " + filepath)
        return
    data = np.load(filepath)
    H_vals = data["H_vals"]
    Ns_species_bound = data["Ns_species_bound"]
    Ns_Ne_60 = data["Ns_Ne_60"]
    Ns_dyn_const = data["Ns_dyn_const"]
    Ns_dyn_log = data["Ns_dyn_log"]
    Ns_dyn_power_05 = data["Ns_dyn_power_0.5"]
    Ns_dyn_power_10 = data["Ns_dyn_power_1.0"]
    Ns_dyn_power_20 = data["Ns_dyn_power_2.0"]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.fill_between(H_vals, Ns_species_bound, 1e15, color='red', alpha=0.2, label='Forbidden Region (Species Bound Violated)')
    ax.fill_between(H_vals, Ns_Ne_60, Ns_species_bound, color='orange', alpha=0.3, label='Quantum Breaking Region (N_e < 60)')
    ax.fill_between(H_vals, 1e-2, Ns_Ne_60, color='green', alpha=0.1, label='Stability Corridor (N_e >= 60)')
    Ns_Ne_30 = 1.0 / (30.0 * H_vals**2)
    Ns_Ne_100 = 1.0 / (100.0 * H_vals**2)
    ax.plot(H_vals, Ns_Ne_30, 'k--', alpha=0.7, label='N_e = 30')
    ax.plot(H_vals, Ns_Ne_60, 'k--', linewidth=2, label='N_e = 60 (Constraint)')
    ax.plot(H_vals, Ns_Ne_100, 'k--', alpha=0.7, label='N_e = 100')
    ax.plot(H_vals, Ns_dyn_const, color='blue', linestyle='-', linewidth=2, label='Dyn. Sel.: F(x) = 1')
    ax.plot(H_vals, Ns_dyn_log, color='cyan', linestyle='-', linewidth=2, label='Dyn. Sel.: F(x) = ln(x)')
    ax.plot(H_vals, Ns_dyn_power_05, color='magenta', linestyle='-', linewidth=2, label='Dyn. Sel.: F(x) = x^0.5')
    ax.plot(H_vals, Ns_dyn_power_10, color='purple', linestyle='-', linewidth=2, label='Dyn. Sel.: F(x) = x^1.0')
    ax.plot(H_vals, Ns_dyn_power_20, color='darkgreen', linestyle='-', linewidth=2, label='Dyn. Sel.: F(x) = x^2.0')
    ax.axvspan(1e-5, 1e-4, color='gray', alpha=0.3, label='Observed Range (10^-5 - 10^-4)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([1e-6, 1e-2])
    ax.set_ylim([1e-1, 1e14])
    ax.set_xlabel('Hubble Parameter H/M_Pl (dimensionless)')
    ax.set_ylabel('Number of Species N_s (dimensionless)')
    ax.set_title('Phase Diagram of the Inflationary Parameter Space')
    ax.grid(True, which='both', ls='--', alpha=0.5)
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
    fig.tight_layout()
    timestamp = int(time.time())
    plot_filename = "phase_diagram_4_" + str(timestamp) + ".png"
    plot_filepath = os.path.join(data_dir, plot_filename)
    fig.savefig(plot_filepath, dpi=300)
    print("Phase diagram saved to " + plot_filepath)
    H_obs_min = 1e-5
    H_obs_max = 1e-4
    Ns_max_species_min_H = 1.0 / (H_obs_min**2)
    Ns_max_species_max_H = 1.0 / (H_obs_max**2)
    Ns_max_Ne60_min_H = 1.0 / (60.0 * H_obs_min**2)
    Ns_max_Ne60_max_H = 1.0 / (60.0 * H_obs_max**2)
    print("\nKey Statistics for the Observationally Motivated Range (H/M_Pl in [10^-5, 10^-4]):")
    print("  At H/M_Pl = 10^-5:")
    print("    Max N_s (Species Bound) = " + str(Ns_max_species_min_H))
    print("    Max N_s (N_e = 60 Constraint) = " + str(Ns_max_Ne60_min_H))
    print("  At H/M_Pl = 10^-4:")
    print("    Max N_s (Species Bound) = " + str(Ns_max_species_max_H))
    print("    Max N_s (N_e = 60 Constraint) = " + str(Ns_max_Ne60_max_H))

if __name__ == '__main__':
    generate_phase_diagram()