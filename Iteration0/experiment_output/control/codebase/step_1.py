# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
from scipy.integrate import solve_ivp
import os

def simulate_graviton_condensate():
    gamma_values = [0.1, 1.0, 10.0]
    Ns_values = [10, 100, 1000]
    H0 = 1e-2
    N0 = 1.0 / (H0**2)
    Q0 = 0.0
    data_dir = "data/"
    results = {}
    print("Fixed point condition dN/dt = 0 implies Q_mem* = N^(5/2) / gamma.")
    print("Therefore, the plateau value of Q_mem/N is N^(3/2) / gamma.\n")
    for gamma in gamma_values:
        for Ns in Ns_values:
            t_qb = (N0**1.5) / Ns
            t_max = max(3.0 * t_qb, 2.0 * (N0**1.5))
            t_span = (0, t_max)
            def system(t, y):
                N, Q = y
                if N <= 1e-10:
                    return [0.0, 0.0]
                dN_dt = -1.0 / np.sqrt(N) + gamma * Q / (N**2)
                dQ_dt = Ns / np.sqrt(N)
                return [dN_dt, dQ_dt]
            def stop_event(t, y):
                return y[0] - 1e-5
            stop_event.terminal = True
            sol = solve_ivp(system, t_span, [N0, Q0], method='Radau', rtol=1e-8, atol=1e-10, events=stop_event)
            t = sol.t
            N = sol.y[0]
            Q = sol.y[1]
            N_safe = np.maximum(N, 1e-10)
            H = 1.0 / np.sqrt(N_safe)
            dN_dt = -1.0 / np.sqrt(N_safe) + gamma * Q / (N_safe**2)
            idx_min_dN = np.argmin(np.abs(dN_dt))
            Q_N_num = Q[idx_min_dN] / N_safe[idx_min_dN]
            N_plateau = N_safe[idx_min_dN]
            Q_N_ana = (N_plateau**1.5) / gamma
            print("gamma=" + str(gamma) + ", Ns=" + str(Ns) + ":")
            print("  t_qb = " + str(t_qb))
            print("  Numerically observed plateau Q_mem/N = " + str(Q_N_num))
            print("  Analytical prediction N^(3/2)/gamma = " + str(Q_N_ana))
            print("  Difference = " + str(abs(Q_N_num - Q_N_ana)) + "\n")
            key = "gamma_" + str(gamma) + "_Ns_" + str(Ns)
            results[key + "_t"] = t
            results[key + "_N"] = N
            results[key + "_Q"] = Q
            results[key + "_H"] = H
    filepath = os.path.join(data_dir, "graviton_condensate_sim.npz")
    np.savez(filepath, **results)
    print("Data saved to " + filepath)

if __name__ == '__main__':
    simulate_graviton_condensate()