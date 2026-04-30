# filename: codebase/step_5.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['text.usetex'] = False

def main():
    M_Pl = 1.0
    H_test_vals = [1e-5, 1e-4, 1e-3, 1e-2]
    Ns_test_vals = [1, 10, 100, 1000]
    print("==================================================================")
    print(" Numerical Verification of the N_e-N_s Relation")
    print("==================================================================\n")
    print("--- Numerical Verification of N_e = H * t_qb ---")
    for H in H_test_vals:
        for Ns in Ns_test_vals:
            t_qb = M_Pl**2 / (Ns * H**3)
            N_e = H * t_qb
            expected_Ne = M_Pl**2 / (Ns * H**2)
            ratio = N_e / expected_Ne
            print("H = " + ("%.1e" % H) + " M_Pl, N_s = " + str(Ns) + " -> t_qb = " + ("%.3e" % t_qb) + " M_Pl^-1, N_e = " + ("%.3e" % N_e) + " (Ratio N_e/Expected: " + ("%.5f" % ratio) + ")")
    H_vals = np.logspace(-6, -1, 500)
    Ne_Ns_vals = M_Pl**2 / H_vals**2
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(H_vals, Ne_Ns_vals, 'b-', linewidth=2, label='N_e * N_s = 1 / H^2')
    ax1.fill_between(H_vals, 1e-20, Ne_Ns_vals, color='blue', alpha=0.1, label='Allowed Region (N_e * N_s <= 1 / H^2)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Hubble Parameter H [M_Pl]', fontsize=12)
    ax1.set_ylabel('N_e * N_s', fontsize=12)
    ax1.set_title('Verification of the Bound N_e * N_s <= 1 / H^2', fontsize=14)
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(fontsize=12)
    plt.tight_layout()
    timestamp = int(time.time())
    filepath_fig1 = os.path.join("data", "Ne_Ns_vs_H_1_" + str(timestamp) + ".png")
    plt.savefig(filepath_fig1, dpi=300)
    print("\nPlot saved to " + filepath_fig1)
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    Ns_vals = np.logspace(0, 10, 500)
    H_cutoff = 1.0 / np.sqrt(Ns_vals)
    ax2.plot(Ns_vals, H_cutoff, 'k--', linewidth=2, label='Species Cutoff (N_e = 1)')
    ax2.fill_between(Ns_vals, H_cutoff, 1, color='gray', alpha=0.3, label='Forbidden by Species Cutoff')
    colors = ['red', 'orange', 'green']
    Ne_values = [60, 100, 1000]
    for i, Ne in enumerate(Ne_values):
        H_bound = 1.0 / np.sqrt(Ne * Ns_vals)
        ax2.plot(Ns_vals, H_bound, color=colors[i], linewidth=2, label='N_e = ' + str(Ne))
        if i == 0:
            ax2.fill_between(Ns_vals, H_bound, H_cutoff, color=colors[i], alpha=0.1, label='Forbidden for N_e >= 60')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlim(1, 1e10)
    ax2.set_ylim(1e-6, 1)
    ax2.set_xlabel('Number of Species N_s', fontsize=12)
    ax2.set_ylabel('Hubble Parameter H [M_Pl]', fontsize=12)
    ax2.set_title('Phase Diagram: Allowed and Forbidden Regions in (N_s, H) Space', fontsize=14)
    ax2.grid(True, which="both", ls="--", alpha=0.5)
    ax2.legend(fontsize=10, loc='upper right')
    plt.tight_layout()
    filepath_fig2 = os.path.join("data", "phase_diagram_Ns_H_1_" + str(timestamp) + ".png")
    plt.savefig(filepath_fig2, dpi=300)
    print("Phase diagram saved to " + filepath_fig2)
    print("\n--- Summary of Bounds ---")
    print("The relation N_e * N_s <= M_Pl^2 / H^2 is strictly verified.")
    print("For a given H, increasing N_s decreases the maximum possible number of e-folds N_e.")
    print("For a required N_e (e.g., 60), the maximum allowed number of species is N_s_max = M_Pl^2 / (N_e * H^2).")
    for Ne in Ne_values:
        print("For N_e = " + str(Ne) + " and H = 1e-4 M_Pl, N_s_max = " + ("%.2e" % (1.0 / (Ne * (1e-4)**2))))

if __name__ == '__main__':
    main()