# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import matplotlib.pyplot as plt

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = "data"
    H_vals = np.logspace(-6, -1, 1000)
    x = 1.0 / H_vals
    F_const = np.ones_like(x)
    F_log = np.log(x)
    F_pow_05 = x**0.5
    F_pow_1 = x**1.0
    F_pow_2 = x**2.0
    Ns_const = 1.0 / (H_vals**2 * F_const)
    Ns_log = 1.0 / (H_vals**2 * F_log)
    Ns_pow_05 = 1.0 / (H_vals**2 * F_pow_05)
    Ns_pow_1 = 1.0 / (H_vals**2 * F_pow_1)
    Ns_pow_2 = 1.0 / (H_vals**2 * F_pow_2)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(H_vals, Ns_const, label='Constant: F = 1 (Unique H for given N_s)', linewidth=2)
    ax.plot(H_vals, Ns_log, label='Logarithmic: F = ln(1/H) (Unique H for given N_s)', linewidth=2)
    ax.plot(H_vals, Ns_pow_05, label='Power-law delta=0.5: F = (1/H)^0.5 (Unique H for given N_s)', linewidth=2)
    ax.plot(H_vals, Ns_pow_1, label='Power-law delta=1: F = 1/H (Unique H for given N_s)', linewidth=2)
    ax.plot(H_vals, Ns_pow_2, label='Power-law delta=2: F = (1/H)^2 (Family of solutions for N_s=1)', linewidth=2, linestyle='--')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Hubble Scale H / M_Pl', fontsize=14)
    ax.set_ylabel('Number of Species N_s', fontsize=14)
    ax.set_title('Dynamical Selection: N_s vs H for various F(1/H)', fontsize=16)
    ax.set_xlim(1e-6, 1e-1)
    ax.set_ylim(1e0, 1e13)
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend(fontsize=11, loc='upper right')
    plt.tight_layout()
    timestamp = int(time.time())
    plot_filename = os.path.join(data_dir, "dynamical_selection_3_" + str(timestamp) + ".png")
    plt.savefig(plot_filename, dpi=300)
    print("Plot saved to " + plot_filename)
    data_filename = os.path.join(data_dir, "selection_data.npz")
    np.savez_compressed(data_filename, H_vals=H_vals, Ns_const=Ns_const, Ns_log=Ns_log, Ns_pow_05=Ns_pow_05, Ns_pow_1=Ns_pow_1, Ns_pow_2=Ns_pow_2)
    print("Sweep results saved to " + data_filename)
    print("\n--- Dynamical Selection Parameter Sweep ---")
    print("Equation: N_s * F(1/H) = 1/H^2")
    print("Evaluated over H from 1e-6 to 1e-1.")
    idx_1e5 = np.argmin(np.abs(H_vals - 1e-5))
    print("\nKey results at H ~ 1e-5:")
    print("  Constant F=1: N_s = " + str(Ns_const[idx_1e5]))
    print("  Logarithmic F=ln(1/H): N_s = " + str(Ns_log[idx_1e5]))
    print("  Power-law delta=0.5: N_s = " + str(Ns_pow_05[idx_1e5]))
    print("  Power-law delta=1.0: N_s = " + str(Ns_pow_1[idx_1e5]))
    print("  Power-law delta=2.0: N_s = " + str(Ns_pow_2[idx_1e5]))
    idx_1e2 = np.argmin(np.abs(H_vals - 1e-2))
    print("\nKey results at H ~ 1e-2:")
    print("  Constant F=1: N_s = " + str(Ns_const[idx_1e2]))
    print("  Logarithmic F=ln(1/H): N_s = " + str(Ns_log[idx_1e2]))
    print("  Power-law delta=0.5: N_s = " + str(Ns_pow_05[idx_1e2]))
    print("  Power-law delta=1.0: N_s = " + str(Ns_pow_1[idx_1e2]))
    print("  Power-law delta=2.0: N_s = " + str(Ns_pow_2[idx_1e2]))
    print("\nConclusion on solutions:")
    print("- For F(1/H) = (1/H)^2, N_s is identically 1 for all H. This means for N_s = 1, there is a family of solutions (any H is allowed), while for N_s != 1, there are no solutions.")
    print("- For all other tested forms of F, N_s(H) is strictly monotonic, meaning for a given N_s, there is a unique solution for H.")

if __name__ == '__main__':
    main()