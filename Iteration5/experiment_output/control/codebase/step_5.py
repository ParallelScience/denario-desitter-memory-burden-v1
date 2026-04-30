# filename: codebase/step_5.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import pandas as pd
import os

def compute_dynamical_selection_and_reheating():
    print("Starting computation of dynamical selection and reheating...")
    H_vals = np.logspace(-8, -1, 1000)
    results = []
    M_Pl_GeV = 1.22e19
    for H in H_vals:
        x = 1.0 / H
        F1 = 1.0
        Ns_1 = 1.0 / (H**2 * F1)
        F2 = np.log(x)
        Ns_2 = 1.0 / (H**2 * F2)
        F3 = x
        Ns_3 = 1.0 / (H**2 * F3)
        for f_type, Ns in [('constant', Ns_1), ('logarithmic', Ns_2), ('linear', Ns_3)]:
            if Ns < 1:
                continue
            t_qb = 1.0 / (Ns * H**3)
            Gamma = Ns**(-1.5)
            g_star = Ns
            T_rh_Pl = (90.0 / (np.pi**2 * g_star))**0.25 * np.sqrt(Gamma)
            T_rh_GeV = T_rh_Pl * M_Pl_GeV
            results.append({'H': H, 'F_type': f_type, 'N_s': Ns, 't_qb': t_qb, 'Gamma': Gamma, 'T_rh_Pl': T_rh_Pl, 'T_rh_GeV': T_rh_GeV})
    df = pd.DataFrame(results)
    csv_path = os.path.join('data', 'dynamical_selection_reheating.csv')
    df.to_csv(csv_path, index=False)
    print("Computation complete. Data saved to " + csv_path)
    print("\n--- Summary of Reheating Temperatures ---")
    target_Hs = [1e-6, 1e-5, 1e-4, 1e-3]
    for target_H in target_Hs:
        print("\nFor H ~ " + str(target_H) + " M_Pl:")
        closest_H = df['H'].iloc[(df['H'] - target_H).abs().argsort().iloc[0]]
        subset = df[df['H'] == closest_H]
        for _, row in subset.iterrows():
            f_type = row['F_type']
            Ns = row['N_s']
            t_qb = row['t_qb']
            Gamma = row['Gamma']
            T_rh_Pl = row['T_rh_Pl']
            T_rh_GeV = row['T_rh_GeV']
            Ns_str = "%.2e" % Ns
            t_qb_str = "%.2e" % t_qb
            Gamma_str = "%.2e" % Gamma
            T_rh_Pl_str = "%.2e" % T_rh_Pl
            T_rh_GeV_str = "%.2e" % T_rh_GeV
            f_type_padded = f_type + " " * (12 - len(f_type))
            print("  F(x) = " + f_type_padded + " | N_s = " + Ns_str + " | t_qb = " + t_qb_str + " | Gamma = " + Gamma_str + " | T_rh = " + T_rh_Pl_str + " M_Pl = " + T_rh_GeV_str + " GeV")

if __name__ == '__main__':
    compute_dynamical_selection_and_reheating()