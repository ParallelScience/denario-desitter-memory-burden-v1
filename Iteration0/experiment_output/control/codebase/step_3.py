# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import os

def compute_constraints_and_equilibrium():
    data_dir = "data/"
    H_vals = np.logspace(-6, -2, 1000)
    Ns_species_bound = 1.0 / (H_vals**2)
    Ne = 60
    Ns_Ne_60 = 1.0 / (Ne * (H_vals**2))
    Ns_dyn_const = 1.0 / (H_vals**2 * 1.0)
    Ns_dyn_log = 1.0 / (H_vals**2 * np.log(1.0 / H_vals))
    p_values = [0.5, 1.0, 2.0]
    Ns_dyn_power = {}
    for p in p_values:
        Ns_dyn_power[p] = 1.0 / (H_vals**2 * (1.0 / H_vals)**p)
    print("Intersections of dynamical selection curves with N_e = 60 constraint line:")
    print("  (a) F(x) = 1: No intersection (1 != 60)")
    H_int_log = np.exp(-60)
    Ns_int_log = 1.0 / (Ne * (H_int_log**2))
    print("  (b) F(x) = ln(1/H): H = " + str(H_int_log) + " M_Pl, N_s = " + str(Ns_int_log))
    for p in p_values:
        H_int_power = 60.0**(-1.0 / p)
        Ns_int_power = 1.0 / (Ne * (H_int_power**2))
        print("  (c) F(x) = (1/H)^" + str(p) + ": H = " + str(H_int_power) + " M_Pl, N_s = " + str(Ns_int_power))
    results = {
        "H_vals": H_vals,
        "Ns_species_bound": Ns_species_bound,
        "Ns_Ne_60": Ns_Ne_60,
        "Ns_dyn_const": Ns_dyn_const,
        "Ns_dyn_log": Ns_dyn_log,
    }
    for p in p_values:
        results["Ns_dyn_power_" + str(p)] = Ns_dyn_power[p]
    filepath = os.path.join(data_dir, "constraint_boundaries.npz")
    np.savez(filepath, **results)
    print("\nData saved to " + filepath)

if __name__ == '__main__':
    compute_constraints_and_equilibrium()