# filename: codebase/step_6.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['text.usetex'] = False

def solve_H_const(Ns):
    return 1.0 / np.sqrt(Ns)

def solve_H_log(Ns):
    if Ns < 2 * np.exp(1):
        return np.nan
    def f(x):
        return x**2 - Ns * np.log(x)
    x_min = np.sqrt(Ns / 2.0)
    x_high = x_min * 2.0
    while f(x_high) < 0:
        x_high *= 2.0
    res = root_scalar(f, bracket=[x_min, x_high])
    if res.converged:
        return 1.0 / res.root
    return np.nan

def solve_H_sqrt(Ns):
    return Ns**(-2/3)

def main():
    print("==================================================================")
    print(" Dynamical Selection Analysis and Extended Phase Space Mapping")
    print("==================================================================\n")
    print("--- Dynamical Selection Analysis ---")
    print("Equation: N_s * F(1/H) = 1/H^2")
    print("For F = const (e.g., F=1): H = 1/sqrt(N_s). Yields a unique preferred H matching the species cutoff.")
    print("For F = ln(1/H): The equation x^2 = N_s * ln(x) (with x = 1/H) has solutions only for N_s >= 2e (~5.44).")
    print("                 For N_s >= 2e, it yields two solutions; we select the one with smaller H (larger x).")
    print("For F = (1/H)^0.5: The equation x^2 = N_s * x^0.5 yields a unique preferred H = N_s^(-2/3).\n")
    print("Conclusion on uniqueness:")
    print("By treating the dynamical selection condition as an exact equation N_s * F(1/H) = 1/H^2,")
    print("each functional form yields a unique preferred H (when a solution exists), rather than an inequality.")
    print("However, if the condition is interpreted as a bound Q_mem <= N, it would yield an inequality H <= H_pref.\n")
    Ns_test = [1, 10, 100, 10**8]
    print("--- Preferred H values and resulting N_e for different F(1/H) ---")
    for Ns in Ns_test:
        H_const = solve_H_const(Ns)
        H_log = solve_H_log(Ns)
        H_sqrt = solve_H_sqrt(Ns)
        Ne_const = 1.0 / (Ns * H_const**2) if H_const > 0 else np.nan
        Ne_log = 1.0 / (Ns * H_log**2) if not np.isnan(H_log) else np.nan
        Ne_sqrt = 1.0 / (Ns * H_sqrt**2) if H_sqrt > 0 else np.nan
        H_log_str = ("%.3e" % H_log) if not np.isnan(H_log) else "No solution"
        Ne_log_str = ("%.1f" % Ne_log) if not np.isnan(Ne_log) else "N/A"
        print("N_s = " + str(Ns) + ":")
        print("  F = const     -> H = " + ("%.3e" % H_const) + " M_Pl  => N_e = " + ("%.1f" % Ne_const))
        print("  F = ln(1/H)   -> H = " + H_log_str + " M_Pl  => N_e = " + Ne_log_str)
        print("  F = (1/H)^0.5 -> H = " + ("%.3e" % H_sqrt) + " M_Pl  => N_e = " + ("%.1f" % Ne_sqrt))
        print("")
    Ns_vals = np.logspace(0, 10, 1000)
    H_cutoff = 1.0 / np.sqrt(Ns_vals)
    H_Ne60 = 1.0 / np.sqrt(60 * Ns_vals)
    H_Ne100 = 1.0 / np.sqrt(100 * Ns_vals)
    H_Ne1000 = 1.0 / np.sqrt(1000 * Ns_vals)
    H_sel_const = 1.0 / np.sqrt(Ns_vals)
    H_sel_sqrt = Ns_vals**(-2/3)
    H_sel_log = np.zeros_like(Ns_vals)
    for i, Ns in enumerate(Ns_vals):
        H_sel_log[i] = solve_H_log(Ns)
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.fill_between(Ns_vals, H_cutoff, 1, color='gray', alpha=0.3, label='Forbidden (Species Cutoff: N_s > 1/H^2)')
    ax.plot(Ns_vals, H_cutoff, 'k--', linewidth=2, label='Species Cutoff (N_e = 1)')
    colors_Ne = ['red', 'orange', 'green']
    Ne_values = [60, 100, 1000]
    H_bounds = [H_Ne60, H_Ne100, H_Ne1000]
    for i, Ne in enumerate(Ne_values):
        ax.plot(Ns_vals, H_bounds[i], color=colors_Ne[i], linestyle='-.', linewidth=2, label='Max H for N_e = ' + str(Ne))
        if i == 0:
            ax.fill_between(Ns_vals, H_bounds[i], H_cutoff, color='red', alpha=0.1, label='Insufficient Inflation (N_e < 60)')
    ax.plot(Ns_vals, H_sel_const, color='blue', linestyle=':', linewidth=3, label='Selection: F = const')
    valid_log = ~np.isnan(H_sel_log)
    ax.plot(Ns_vals[valid_log], H_sel_log[valid_log], color='purple', linestyle='-', linewidth=2, label='Selection: F = ln(1/H)')
    ax.plot(Ns_vals, H_sel_sqrt, color='cyan', linestyle='-', linewidth=2, label='Selection: F = (1/H)^0.5')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1, 1e10)
    ax.set_ylim(1e-8, 1)
    ax.set_xlabel('Number of Species N_s', fontsize=14)
    ax.set_ylabel('Hubble Parameter H [M_Pl]', fontsize=14)
    ax.set_title('Extended Phase Space Diagram and Dynamical Selection', fontsize=16)
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend(fontsize=11, loc='lower left')
    plt.tight_layout()
    timestamp = int(time.time())
    filepath = os.path.join("data", "extended_phase_diagram_1_" + str(timestamp) + ".png")
    plt.savefig(filepath, dpi=300)
    print("Extended phase diagram saved to " + filepath)

if __name__ == '__main__':
    main()