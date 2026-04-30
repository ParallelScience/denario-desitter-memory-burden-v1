# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter

def compute_perturbations():
    print("Starting perturbation spectrum computation...")
    start_time = time.time()
    gamma_vals = [0.1, 1.0, 10.0]
    alpha_vals = [0.1, 1.0, 10.0]
    Ns_vals = [1, 100, 10000, 1000000]
    H0_vals = [1e-5, 1e-4, 1e-3, 1e-2]
    results = []
    total_combinations = len(gamma_vals) * len(alpha_vals) * len(Ns_vals) * len(H0_vals)
    count = 0
    for gamma in gamma_vals:
        for alpha in alpha_vals:
            for N_s in Ns_vals:
                for H0 in H0_vals:
                    count += 1
                    H0_sq = H0**2
                    beta = gamma * alpha * N_s * H0**3
                    def system_tau(tau, y):
                        n, q, Ne = y
                        if n <= 1e-15:
                            return [0.0, 0.0, 0.0]
                        n_inv_half = n**(-0.5)
                        dn = H0_sq * (-n_inv_half + q / n**2)
                        dq = beta * n_inv_half
                        dNe = n_inv_half
                        return [dn, dq, dNe]
                    def jac_tau(tau, y):
                        n, q, Ne = y
                        if n <= 1e-15:
                            return np.zeros((3, 3))
                        n_inv_1_5 = n**(-1.5)
                        n_inv_2 = n**(-2.0)
                        n_inv_3 = n**(-3.0)
                        d_dn_dn = H0_sq * (0.5 * n_inv_1_5 - 2.0 * q * n_inv_3)
                        d_dn_dq = H0_sq * n_inv_2
                        d_dn_dNe = 0.0
                        d_dq_dn = -0.5 * beta * n_inv_1_5
                        d_dq_dq = 0.0
                        d_dq_dNe = 0.0
                        d_dNe_dn = -0.5 * n_inv_1_5
                        d_dNe_dq = 0.0
                        d_dNe_dNe = 0.0
                        return [[d_dn_dn, d_dn_dq, d_dn_dNe], [d_dq_dn, d_dq_dq, d_dq_dNe], [d_dNe_dn, d_dNe_dq, d_dNe_dNe]]
                    def event_bounce_tau(tau, y):
                        n, q, Ne = y
                        if n <= 1e-15:
                            return -1.0
                        return -n**(-0.5) + q / n**2
                    event_bounce_tau.terminal = True
                    event_bounce_tau.direction = 1
                    def event_zero_tau(tau, y):
                        return y[0] - 1e-12
                    event_zero_tau.terminal = True
                    tau_max_1 = 1e15
                    sol1 = solve_ivp(system_tau, [0, tau_max_1], [1.0, 0.0, 0.0], events=[event_bounce_tau, event_zero_tau], jac=jac_tau, method='Radau', rtol=1e-11, atol=1e-11)
                    if sol1.status == 1 and len(sol1.t_events[0]) > 0:
                        tau_bounce = sol1.t_events[0][0]
                        y_bounce = sol1.y_events[0][0]
                        Ne_bounce = y_bounce[2]
                        Ne_target = Ne_bounce + 60.0
                        Ne_stop = Ne_bounce + 61.0
                        def event_Ne_stop(tau, y):
                            return y[2] - Ne_stop
                        event_Ne_stop.terminal = True
                        tau_max_2 = tau_bounce + 1e15
                        sol2 = solve_ivp(system_tau, [tau_bounce, tau_max_2], y_bounce, events=[event_Ne_stop], jac=jac_tau, dense_output=True, method='Radau', rtol=1e-12, atol=1e-12)
                        if sol2.status == 1 and len(sol2.t_events[0]) > 0:
                            tau_stop = sol2.t_events[0][0]
                            tau_grid = np.linspace(tau_bounce, tau_stop, 5000)
                            y_grid = sol2.sol(tau_grid)
                            n_grid = y_grid[0]
                            Ne_grid = y_grid[2]
                            if np.all(n_grid > 0):
                                H_grid = H0 / np.sqrt(n_grid)
                                t_grid = tau_grid / H0
                                window_length = 51
                                polyorder = 3
                                H_smooth = savgol_filter(H_grid, window_length, polyorder)
                                dot_H = np.gradient(H_smooth, t_grid)
                                epsilon_grid = -dot_H / H_smooth**2
                                epsilon_smooth = savgol_filter(epsilon_grid, window_length, polyorder)
                                dot_epsilon = np.gradient(epsilon_smooth, t_grid)
                                valid_mask = epsilon_smooth > 1e-25
                                if np.any(valid_mask):
                                    eta_grid = np.zeros_like(epsilon_smooth)
                                    eta_grid[valid_mask] = dot_epsilon[valid_mask] / (H_smooth[valid_mask] * epsilon_smooth[valid_mask])
                                    idx_target = np.argmin(np.abs(Ne_grid - Ne_target))
                                    epsilon = epsilon_smooth[idx_target]
                                    eta = eta_grid[idx_target]
                                    n_s = 1.0 - 6.0 * epsilon + 2.0 * eta
                                    r = 16.0 * epsilon
                                    if np.isnan(n_s) or np.isinf(n_s) or np.isnan(r) or np.isinf(r):
                                        n_s = np.nan
                                        r = np.nan
                                else:
                                    n_s = np.nan
                                    r = np.nan
                            else:
                                n_s = np.nan
                                r = np.nan
                        else:
                            n_s = np.nan
                            r = np.nan
                    else:
                        n_s = np.nan
                        r = np.nan
                    results.append({'gamma': gamma, 'alpha': alpha, 'N_s': N_s, 'H0': H0, 'n_s': n_s, 'r': r})
                    if count % 20 == 0 or count == total_combinations:
                        print("Processed " + str(count) + "/" + str(total_combinations) + " combinations.")
    df = pd.DataFrame(results)
    csv_path = "data/perturbation_spectrum.csv"
    df.to_csv(csv_path, index=False)
    elapsed = time.time() - start_time
    print("\nGrid computation complete in " + str(round(elapsed, 2)) + " seconds.")
    print("Data saved to " + csv_path)
    valid_results = df.dropna().copy()
    print("\nSummary of valid results:")
    if len(valid_results) > 0:
        print("Total valid combinations: " + str(len(valid_results)))
        print("n_s range: [" + str(round(valid_results['n_s'].min(), 6)) + ", " + str(round(valid_results['n_s'].max(), 6)) + "]")
        print("r range: [" + str(valid_results['r'].min()) + ", " + str(valid_results['r'].max()) + "]")
        print("\nSample of results (closest to n_s = 0.96):")
        valid_results['ns_diff'] = np.abs(valid_results['n_s'] - 0.96)
        closest = valid_results.sort_values('ns_diff').head(5)
        for _, row in closest.iterrows():
            print("gamma=" + str(row['gamma']) + ", alpha=" + str(row['alpha']) + ", N_s=" + str(row['N_s']) + ", H0=" + str(row['H0']) + " -> n_s=" + str(round(row['n_s'], 4)) + ", r=" + str(row['r']))
    else:
        print("No valid results found.")

if __name__ == '__main__':
    compute_perturbations()