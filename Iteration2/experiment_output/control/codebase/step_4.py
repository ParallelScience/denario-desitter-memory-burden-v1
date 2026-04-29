# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
from scipy.integrate import solve_ivp
import time
import os

def ode_system(t, y, H, N_s, gamma):
    N, Q_mem = y
    if N <= 0:
        return [0.0, N_s * H]
    dN_dt = -H + gamma * Q_mem / (N**2)
    dQ_mem_dt = N_s * H
    return [dN_dt, dQ_mem_dt]

def event_quantum_breaking(t, y, H, N_s, gamma):
    return y[1] - y[0]
event_quantum_breaking.terminal = True
event_quantum_breaking.direction = 1

def event_N_zero(t, y, H, N_s, gamma):
    return y[0] - 1e-5
event_N_zero.terminal = True

def main():
    data_dir = "data"
    num_points = 30
    N_s_vals = np.logspace(0, 8, num_points)
    H_vals = np.logspace(-5, -2, num_points)
    N_e_matrix = np.zeros((num_points, num_points))
    print("--- Starting Numerical Simulation of the Stability Corridor ---")
    start_time = time.time()
    for i, N_s in enumerate(N_s_vals):
        for j, H in enumerate(H_vals):
            gamma = 1.0 / (H**3)
            N0 = 1.0 / (H**2)
            Q0 = 0.0
            t_est = N0 / (N_s * H)
            t_max = 10.0 * t_est
            sol = solve_ivp(ode_system, [0, t_max], [N0, Q0], args=(H, N_s, gamma), events=[event_quantum_breaking, event_N_zero], method='LSODA', rtol=1e-5, atol=1e-5)
            if sol.status == 1 and len(sol.t_events[0]) > 0:
                t_qb = sol.t_events[0][0]
                N_e = H * t_qb
            elif len(sol.t_events[1]) > 0:
                t_qb = sol.t_events[1][0]
                N_e = H * t_qb
            else:
                N_e = H * t_max
            N_e_matrix[i, j] = N_e
    end_time = time.time()
    print("Integration completed in " + str(round(end_time - start_time, 2)) + " seconds.")
    data_filename = os.path.join(data_dir, "simulation_data.npz")
    np.savez_compressed(data_filename, N_s_vals=N_s_vals, H_vals=H_vals, N_e_matrix=N_e_matrix)
    print("Simulation data saved to " + data_filename)
    print("\n--- Simulation Results Summary ---")
    print("N_e min: " + str(np.min(N_e_matrix)))
    print("N_e max: " + str(np.max(N_e_matrix)))
    valid_points = np.sum(N_e_matrix >= 60)
    total_points = N_e_matrix.size
    percentage = round(valid_points / total_points * 100, 2)
    print("Points with N_e >= 60: " + str(valid_points) + " out of " + str(total_points) + " (" + str(percentage) + "%)")

if __name__ == '__main__':
    main()