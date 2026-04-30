# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.integrate import solve_ivp
from datetime import datetime
import time

def define_and_analyze_system():
    N, Q_mem, gamma, N_s = sp.symbols('N Q_mem gamma N_s', positive=True, real=True)
    dN_dt = -1/sp.sqrt(N) + gamma * Q_mem / N**2
    dQ_mem_dt = N_s / sp.sqrt(N)
    N_nullcline = sp.solve(dN_dt, Q_mem)[0]
    print("Analytical Results:")
    print("-------------------")
    print("Coupled ODEs:")
    print("dN/dt = " + str(dN_dt))
    print("dQ_mem/dt = " + str(dQ_mem_dt))
    print("\nN-nullcline (dN/dt = 0) condition for Q_mem:")
    print("Q_mem* = " + str(N_nullcline))
    gamma_val = 1.0
    N_val = 1e6
    Q_mem_val = float(N_nullcline.subs({N: N_val, gamma: gamma_val}))
    dN_dt_val = float(dN_dt.subs({N: N_val, Q_mem: Q_mem_val, gamma: gamma_val}))
    print("\nNumerical Verification:")
    print("-----------------------")
    print("Parameters: gamma = " + str(gamma_val) + ", N = " + str(N_val))
    print("Calculated Q_mem* = " + str(Q_mem_val))
    print("Evaluated dN/dt at (N, Q_mem*) = " + str(dN_dt_val) + " (Expected: 0.0)\n")
    return N, Q_mem, gamma, N_s, dN_dt, dQ_mem_dt, N_nullcline

def generate_phase_space_plot():
    plt.rcParams['text.usetex'] = False
    gamma_val = 1.0
    N_s_val = 100.0
    log_N_min = 6
    log_N_max = 10
    log_Q_min = 0
    log_Q_max = 10
    log_N_lin = np.linspace(log_N_min, log_N_max, 100)
    log_Q_lin = np.linspace(log_Q_min, log_Q_max, 100)
    N_mesh, Q_mesh = np.meshgrid(10**log_N_lin, 10**log_Q_lin)
    dN_dt_mesh = -1/np.sqrt(N_mesh) + gamma_val * Q_mesh / N_mesh**2
    dQ_dt_mesh = N_s_val / np.sqrt(N_mesh)
    dlogN_dt = dN_dt_mesh / (N_mesh * np.log(10))
    dlogQ_dt = dQ_dt_mesh / (Q_mesh * np.log(10))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.streamplot(log_N_lin, log_Q_lin, dlogN_dt, dlogQ_dt, density=1.5, color='blue', linewidth=1, arrowsize=1.5)
    N_line = np.logspace(log_N_min, log_N_max, 100)
    Q_null = N_line**(1.5) / gamma_val
    ax1.plot(np.log10(N_line), np.log10(Q_null), 'r--', linewidth=2, label='N-nullcline (dN/dt = 0)')
    ax1.plot(np.log10(N_line), np.log10(N_line), 'k:', linewidth=2, label='Quantum Breaking (Q_mem = N)')
    ax1.set_xlabel('log10(N)')
    ax1.set_ylabel('log10(Q_mem)')
    ax1.set_title('Phase-Space Streamplot (gamma=' + str(gamma_val) + ', N_s=' + str(N_s_val) + ')')
    ax1.set_xlim(log_N_min, log_N_max)
    ax1.set_ylim(log_Q_min, log_Q_max)
    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle=':', alpha=0.7)
    def system(t, y):
        N_t, Q_t = y
        if N_t <= 0:
            return [0, 0]
        dN = -1/np.sqrt(N_t) + gamma_val * Q_t / N_t**2
        dQ = N_s_val / np.sqrt(N_t)
        return [dN, dQ]
    def stop_event(t, y):
        return y[0] - 1.0
    stop_event.terminal = True
    initial_conditions = [(1e6, 0.0), (1e8, 0.0), (1e10, 0.0)]
    colors = ['g', 'm', 'c']
    for idx, (N0, Q0) in enumerate(initial_conditions):
        t_max = 2.0 * N0**1.5
        t_eval = np.logspace(0, np.log10(t_max), 500)
        t_eval = np.insert(t_eval, 0, 0)
        sol = solve_ivp(system, (0, t_max), [N0, Q0], t_eval=t_eval, method='RK45', events=stop_event)
        if sol.success or sol.status == 1:
            ax2.plot(sol.t, sol.y[0], color=colors[idx], linestyle='-', label='N(t) for N_0=10^' + str(int(np.log10(N0))))
            ax2.plot(sol.t, sol.y[1], color=colors[idx], linestyle='--', label='Q_mem(t) for N_0=10^' + str(int(np.log10(N0))))
    ax2.set_xscale('symlog', linthresh=1e4)
    ax2.set_yscale('log')
    ax2.set_xlabel('Time t (Planck units)')
    ax2.set_ylabel('Occupation Number N, Memory Load Q_mem')
    ax2.set_title('Time-Series Trajectories')
    ax2.legend(fontsize=8, loc='best')
    ax2.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    timestamp = int(time.time())
    filename = "data/phase_space_analysis_1_" + str(timestamp) + ".png"
    plt.savefig(filename, dpi=300)
    print("Plot saved to " + filename)

if __name__ == '__main__':
    define_and_analyze_system()
    generate_phase_space_plot()