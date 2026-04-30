# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import os

mpl.rcParams['text.usetex'] = False

def main():
    print("==================================================================")
    print(" Verification of Quantum Breaking Time and Central Inequality")
    print("==================================================================\n")
    M_Pl = 1.0
    H_vals = np.logspace(-5, -2, 300)
    Ns_vals = np.logspace(0, 8, 300)
    H_grid, Ns_grid = np.meshgrid(H_vals, Ns_vals)
    t_qb_grid = M_Pl**2 / (Ns_grid * H_grid**3)
    fig, ax = plt.subplots(figsize=(10, 8))
    levels = np.logspace(np.log10(t_qb_grid.min()), np.log10(t_qb_grid.max()), 30)
    contour = ax.contourf(Ns_grid, H_grid, t_qb_grid, levels=levels, locator=mpl.ticker.LogLocator(), cmap='viridis')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label('Quantum Breaking Time t_qb [M_Pl^-1]', fontsize=12)
    contour_lines = ax.contour(Ns_grid, H_grid, t_qb_grid, levels=[1e6, 1e9, 1e12, 1e15], colors='white', alpha=0.5, linestyles='dashed')
    ax.clabel(contour_lines, inline=True, fontsize=10, fmt='%.0e')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Number of Species N_s', fontsize=12)
    ax.set_ylabel('Hubble Parameter H [M_Pl]', fontsize=12)
    ax.set_title('Quantum Breaking Time t_qb as a function of H and N_s', fontsize=14)
    plt.tight_layout()
    timestamp = int(time.time())
    filepath = os.path.join("data", "quantum_breaking_time_1_" + str(timestamp) + ".png")
    plt.savefig(filepath, dpi=300)
    print("Contour plot saved to " + filepath + "\n")
    print("--- Key Values of Quantum Breaking Time t_qb ---")
    test_cases = [(1e-5, 1), (1e-5, 100), (1e-5, 1e6), (1e-4, 1), (1e-4, 100), (1e-4, 1e6), (1e-2, 1), (1e-2, 100)]
    for H_test, Ns_test in test_cases:
        t_qb_test = M_Pl**2 / (Ns_test * H_test**3)
        print("H = " + ("%.1e" % H_test) + " M_Pl, N_s = " + ("%.1e" % Ns_test) + " -> t_qb = " + ("%.3e" % t_qb_test) + " M_Pl^-1")
    print("\n--- Verification of Central Inequality H^2 <= M_Pl^2 / (N_s * N_e) ---")
    print("The central inequality is derived from the requirement that the inflationary")
    print("duration t_life = N_e / H must be less than or equal to the quantum breaking time t_qb.")
    print("t_life <= t_qb  =>  N_e / H <= M_Pl^2 / (N_s * H^3)  =>  H^2 <= M_Pl^2 / (N_s * N_e)")
    N_e_test = 60
    print("\nFor a standard requirement of N_e = " + str(N_e_test) + " e-folds:")
    for Ns_test in [1, 100, 1e4, 1e6, 1e8]:
        H_max = np.sqrt(M_Pl**2 / (Ns_test * N_e_test))
        print("N_s = " + ("%.1e" % Ns_test) + " -> Maximum allowed H = " + ("%.3e" % H_max) + " M_Pl")
    print("\nFor a fixed H = 1.0e-04 M_Pl:")
    H_fixed = 1e-4
    for Ns_test in [1, 100, 1e4, 1e6, 1e8]:
        Ne_max = M_Pl**2 / (Ns_test * H_fixed**2)
        print("N_s = " + ("%.1e" % Ns_test) + " -> Maximum possible e-folds N_e = " + ("%.3e" % Ne_max))
        if Ne_max < 60:
            print("  (Warning: N_e < 60, insufficient inflation for this N_s and H)")

if __name__ == '__main__':
    main()