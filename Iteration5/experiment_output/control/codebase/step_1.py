# filename: codebase/step_1.py
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
                    N0 = 1.0 / H0**2
                    Q0 = 0.0
                    Ne0 = 0.0
                    def system_tau(tau, y):
                        N, Q, Ne = y
                        if N <= 0:
                            return [0, 0, 0]
                        H = N**(-0.5)
                        dN_dtau = (-H + gamma * Q / N**2) / H0
                        dQ_dtau = (alpha * N_s * H) / H0
                        dNe_dtau = H / H0
                        return [dN_dtau, dQ_dtau, dNe_dtau]
                    def event_bounce(tau, y):
                        N, Q, Ne = y
                        if N <= 0:
                            return -1.0
                        H = N**(-0.5)
                        dN_dtau = (-H + gamma * Q / N**2) / H0
                        return dN_dtau
                    event_bounce.terminal = True
                    event_bounce.direction = 1
                    def event_N_zero(tau, y):
                        return y[0] - 1.0
                    event_N_zero.terminal = True
                    tau_est = (H0**-3) / (gamma * alpha * N_s)
                    tau_max_1 = min(max(tau_est * 100, 1e10), 1e20)
                    sol1 = solve_ivp(system_tau, [0, tau_max_1], [N0, Q0, Ne0], events=[event_bounce, event_N_zero], method='Radau', rtol=1e-8, atol=1e-6)
                    if sol1.status == 1 and len(sol1.t_events[0]) > 0:
                        tau_bounce = sol1.t[-1]
                        y_bounce = sol1.y[:, -1]
                        Ne_bounce = y_bounce[2]
                        Ne_target = Ne_bounce + 60.0
                        Ne_stop = Ne_bounce + 61.0
                        def event_Ne_stop(tau, y):
                            return y[2] - Ne_stop
                        event_Ne_stop.terminal = True
                        def event_N_large(tau, y):
                            return 1e20 - y[0]
                        event_N_large.terminal = True
                        tau_max_2 = tau_bounce + 1e5 / H0
                        sol2 = solve_ivp(system_tau, [tau_bounce, tau_max_2], y_bounce, events=[event_Ne_stop, event_N_zero, event_N_large], method='Radau', dense_output=True, rtol=1e-13, atol=1e-13)
                        tau_stop = sol2.t[-1]
                        if tau_stop > tau_bounce + 1e-5:
                            tau_grid = np.linspace(tau_bounce, tau_stop, 5000)
                            y_grid = sol2.sol(tau_grid)
                            N_grid = y_grid[0]
                            Ne_grid = y_grid[2]
                            if np.all(N_grid > 0):
                                t_grid = tau_grid / H0
                                H_grid = N_grid**(-0.5)
                                window_length = min(501, len(H_grid) // 2 * 2 + 1)
                                if window_length > 3:
                                    H_smooth = savgol_filter(H_grid, window_length, 3)
                                else:
                                    H_smooth = H_grid
                                dot_H = np.gradient(H_smooth, t_grid)
                                epsilon_grid = -dot_H / H_smooth**2
                                if window_length > 3:
                                    epsilon_smooth = savgol_filter(epsilon_grid, window_length, 3)
                                else:
                                    epsilon_smooth = epsilon_grid
                                dot_epsilon = np.gradient(epsilon_smooth, t_grid)
                                valid_mask = epsilon_smooth > 1e-25
                                if np.any(valid_mask):
                                    eta_grid = np.zeros_like(epsilon_smooth)
                                    eta_grid[valid_mask] = dot_epsilon[valid_mask] / (H_smooth[valid_mask] * epsilon_smooth[valid_mask])
                                    idx_target = np.argmin(np.abs(Ne_grid - Ne_target))
                                    epsilon = max(epsilon_smooth[idx_target], 1e-25)
                                    eta = eta_grid[idx_target]
                                    n_s = 1 - 6 * epsilon + 2 * eta
                                    r = 16 * epsilon
                                    if abs(n_s) > 10 or np.isnan(n_s):
                                        N_val = N_grid[idx_target]
                                        Q_val = y_grid[1][idx_target]
                                        H_val = N_val**(-0.5)
                                        dN_dt_ana = -H_val + gamma * Q_val / N_val**2
                                        eps_ana = 0.5 * H_val * dN_dt_ana
                                        if eps_ana > 0:
                                            dot_Q_ana = alpha * N_s * H_val
                                            ddot_N_ana = 0.5 * H_val**3 * dN_dt_ana + gamma * dot_Q_ana / N_val**2 - 2 * gamma * Q_val / N_val**3 * dN_dt_ana
                                            dot_H_ana = -0.5 * H_val**3 * dN_dt_ana
                                            dot_eps_ana = 0.5 * dot_H_ana * dN_dt_ana + 0.5 * H_val * ddot_N_ana
                                            eta_ana = dot_eps_ana / (H_val * eps_ana)
                                            n_s = 1 - 6 * eps_ana + 2 * eta_ana
                                            r = 16 * eps_ana
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
    print("\nGrid computation complete. Data saved to " + csv_path)
    valid_results = df.dropna()
    print("\nSummary of valid results:")
    if len(valid_results) > 0:
        print("n_s range: [" + str(valid_results['n_s'].min()) + ", " + str(valid_results['n_s'].max()) + "]")
        print("r range: [" + str(valid_results['r'].min()) + ", " + str(valid_results['r'].max()) + "]")
if __name__ == '__main__':
    compute_perturbations()