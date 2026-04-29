# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import os
import pandas as pd
from scipy.integrate import solve_ivp

def run_simulations():
    N_0 = 1e4
    H_0 = N_0**(-0.5)
    gamma_0 = 1.0
    N_s_values = [10, 100, 1000]
    Q_mem_0 = (N_0**2.5) / gamma_0
    x_0 = Q_mem_0 / N_0
    x_c = x_0 + 1.0
    k_steepness = 100.0
    data_dir = 'data/'
    results = []
    for N_s in N_s_values:
        t_qb_analytical = 1.0 / (N_s * H_0**3)
        N_e_analytical = N_0 / N_s
        def ode_system(t, y):
            N, Q_mem, N_e = y
            N_safe = max(N, 1e-3)
            H = N_safe**(-0.5)
            x = Q_mem / N_safe
            theta = 0.5 * (1.0 - np.tanh(k_steepness * (x - x_c)))
            dN_dt = -H + gamma_0 * Q_mem * (N_safe**(-3)) * theta
            dQ_mem_dt = N_s * H
            dN_e_dt = H
            return [dN_dt, dQ_mem_dt, dN_e_dt]
        def event_quantum_break(t, y):
            N, Q_mem, N_e = y
            N_safe = max(N, 1e-3)
            x = Q_mem / N_safe
            return x - x_c
        event_quantum_break.terminal = False
        event_quantum_break.direction = 1
        def event_N_drop(t, y):
            return y[0] - 1.0
        event_N_drop.terminal = True
        event_N_drop.direction = -1
        t_drop_max = (2.0 / 3.0) * N_0**1.5
        t_end = t_qb_analytical + 1.2 * t_drop_max
        t_span = (0, t_end)
        y0 = [N_0, Q_mem_0, 0.0]
        sol = solve_ivp(ode_system, t_span, y0, method='RK45', events=[event_quantum_break, event_N_drop], max_step=t_qb_analytical / 200.0, dense_output=True, rtol=1e-8, atol=1e-8)
        if len(sol.t_events[0]) > 0:
            t_qb_num = sol.t_events[0][0]
            y_at_t_qb = sol.sol(t_qb_num)
            N_e_num = y_at_t_qb[2]
        else:
            t_qb_num = sol.t[-1]
            N_e_num = sol.y[2][-1]
        df = pd.DataFrame({'time': sol.t, 'N': sol.y[0], 'Q_mem': sol.y[1], 'N_e': sol.y[2], 'H': np.maximum(sol.y[0], 1e-3)**(-0.5)})
        filepath = os.path.join(data_dir, 'time_series_Ns_' + str(N_s) + '.csv')
        df.to_csv(filepath, index=False)
        results.append({'N_s': N_s, 't_qb_analytical': t_qb_analytical, 't_qb_num': t_qb_num, 'N_e_analytical': N_e_analytical, 'N_e_num': N_e_num})
    res_df = pd.DataFrame(results)
    res_filepath = os.path.join(data_dir, 'simulation_summary.csv')
    res_df.to_csv(res_filepath, index=False)

if __name__ == '__main__':
    run_simulations()