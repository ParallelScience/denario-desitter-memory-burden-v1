# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
from scipy.integrate import solve_ivp
from multiprocessing import Pool

def compute_point(args):
    H_init, Ns, gamma = args
    def system_Q(Q_tilde, y):
        N_tilde, tau = y
        if N_tilde < 1e-10:
            N_tilde = 1e-10
        dN_dQ = (-1.0 + gamma * H_init * Q_tilde / (N_tilde**1.5)) / Ns
        dtau_dQ = np.sqrt(N_tilde)
        return [dN_dQ, dtau_dQ]
    def stop_event_Q(Q_tilde, y):
        N_tilde, tau = y
        return N_tilde - Q_tilde
    stop_event_Q.terminal = True
    stop_event_Q.direction = -1
    sol = solve_ivp(system_Q, [0, 2.0], [1.0, 0.0], events=stop_event_Q, dense_output=False, rtol=1e-8, atol=1e-10)
    if sol.status == 1 and len(sol.t_events[0]) > 0:
        Q_qb_tilde = sol.t_events[0][0]
        tau_qb = sol.y_events[0][0, 1]
    else:
        Q_qb_tilde = sol.t[-1]
        tau_qb = sol.y[1, -1]
    N_e = Q_qb_tilde / (Ns * H_init**2)
    t_qb = tau_qb / (Ns * H_init**3)
    return H_init, Ns, N_e, t_qb

if __name__ == '__main__':
    grid_size = 30
    H_init_vals = np.logspace(-5, -2, grid_size)
    Ns_vals = np.logspace(0, 8, grid_size)
    gamma_val = 1.0
    H_grid, Ns_grid = np.meshgrid(H_init_vals, Ns_vals, indexing='ij')
    args_list = [(H, Ns, gamma_val) for H, Ns in zip(H_grid.flatten(), Ns_grid.flatten())]
    print("Starting numerical integration over 30x30 grid...")
    start_time = time.time()
    num_workers = min(16, os.cpu_count() or 1)
    with Pool(num_workers) as pool:
        results = pool.map(compute_point, args_list)
    end_time = time.time()
    print("Integration completed in " + str(round(end_time - start_time, 2)) + " seconds.\n")
    results = np.array(results)
    H_res = results[:, 0].reshape(grid_size, grid_size)
    Ns_res = results[:, 1].reshape(grid_size, grid_size)
    Ne_res = results[:, 2].reshape(grid_size, grid_size)
    tqb_res = results[:, 3].reshape(grid_size, grid_size)
    timestamp = int(time.time())
    filename = "data/inflationary_grid_3_" + str(timestamp) + ".npz"
    np.savez(filename, H_init=H_res, Ns=Ns_res, Ne=Ne_res, t_qb=tqb_res)
    print("Grid data saved to " + filename + "\n")
    print("=== Summary Table: Analytical vs Numerical Results ===")
    header = "H_init".ljust(10) + " | " + "N_s".ljust(10) + " | " + "N_e (Analytic)".ljust(15) + " | " + "N_e (Numeric)".ljust(15) + " | " + "t_qb Ratio (Num/Ana)".ljust(20)
    print(header)
    print("-" * 80)
    indices_to_print = [(0, 0), (0, grid_size//2), (0, grid_size-1), (grid_size//2, 0), (grid_size//2, grid_size//2), (grid_size//2, grid_size-1), (grid_size-1, 0), (grid_size-1, grid_size//2), (grid_size-1, grid_size-1)]
    for i, j in indices_to_print:
        H_val = H_res[i, j]
        Ns_val = Ns_res[i, j]
        Ne_num = Ne_res[i, j]
        tqb_num = tqb_res[i, j]
        Ne_ana = 1.0 / (Ns_val * H_val**2)
        tqb_ana = 1.0 / (Ns_val * H_val**3)
        tqb_ratio = tqb_num / tqb_ana
        H_str = ("%.2e" % H_val).ljust(10)
        Ns_str = ("%.2e" % Ns_val).ljust(10)
        Ne_ana_str = ("%.4e" % Ne_ana).ljust(15)
        Ne_num_str = ("%.4e" % Ne_num).ljust(15)
        ratio_str = ("%.4f" % tqb_ratio).ljust(20)
        print(H_str + " | " + Ns_str + " | " + Ne_ana_str + " | " + Ne_num_str + " | " + ratio_str)