# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import time
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.integrate import solve_ivp

gamma_val = 1
Ns_val = 100

def system(t, y):
    N, Q = y
    if N < 1e-5:
        N = 1e-5
    dN = -1/np.sqrt(N) + gamma_val * Q / N**2
    dQ = Ns_val / np.sqrt(N)
    return [dN, dQ]

def stop_event(t, y):
    return y[0] - 1e-2
stop_event.terminal = True

if __name__ == '__main__':
    N_sym, Q_sym, gamma_sym, Ns_sym = sp.symbols('N Q gamma N_s', positive=True, real=True)
    dN_dt_sym = -1/sp.sqrt(N_sym) + gamma_sym * Q_sym / N_sym**2
    dQ_dt_sym = Ns_sym / sp.sqrt(N_sym)
    N_nullcline = sp.solve(dN_dt_sym, Q_sym)[0]
    N_star_sol = sp.solve(N_nullcline - N_sym, N_sym)
    N_star = N_star_sol[0]
    Q_star = N_star
    J = sp.Matrix([[dN_dt_sym.diff(N_sym), dN_dt_sym.diff(Q_sym)], [dQ_dt_sym.diff(N_sym), dQ_dt_sym.diff(Q_sym)]])
    J_star = J.subs({N_sym: N_star, Q_sym: Q_star})
    eigenvals = J_star.eigenvals()
    evals = list(eigenvals.keys())
    params = {gamma_sym: gamma_val, Ns_sym: Ns_val}
    N_star_num = float(N_star.subs(params).evalf())
    Q_star_num = float(Q_star.subs(params).evalf())
    evals_num = [complex(e.subs(params).evalf()) for e in evals]
    print('=== Analytical Phase-Space Analysis ===')
    print('N-nullcline (dN/dt = 0): Q = ' + str(N_nullcline))
    print('Quasi-stationary state (dN/dt = 0, Q = N):')
    print('  N* = ' + str(N_star))
    print('  Q* = ' + str(Q_star))
    print('\n=== Numerical Evaluation ===')
    print('Parameters: gamma = ' + str(params[gamma_sym]) + ', N_s = ' + str(params[Ns_sym]))
    print('Fixed-point coordinates:')
    print('  N* = ' + str(N_star_num))
    print('  Q* = ' + str(Q_star_num))
    print('Eigenvalues of the Jacobian at the fixed point:')
    for i, ev in enumerate(evals_num):
        print('  lambda_' + str(i+1) + ' = ' + str(ev.real) + ' + ' + str(ev.imag) + 'j')
    if all(ev.real < 0 for ev in evals_num):
        if any(ev.imag != 0 for ev in evals_num):
            print('Conclusion: The fixed point is a STABLE SPIRAL.')
        else:
            print('Conclusion: The fixed point is a STABLE NODE.')
    else:
        print('Conclusion: The fixed point is NOT stable (Saddle or Unstable).')
    logN_vals = np.linspace(-2, 6, 200)
    logQ_vals = np.linspace(-2, 6, 200)
    logN_grid, logQ_grid = np.meshgrid(logN_vals, logQ_vals)
    N_grid = 10**logN_grid
    Q_grid = 10**logQ_grid
    dN_dt_grid = -1/np.sqrt(N_grid) + gamma_val * Q_grid / N_grid**2
    dQ_dt_grid = Ns_val / np.sqrt(N_grid)
    dlogN_dt = dN_dt_grid / (N_grid * np.log(10))
    dlogQ_dt = dQ_dt_grid / (Q_grid * np.log(10))
    magnitude = np.sqrt(dlogN_dt**2 + dlogQ_dt**2)
    magnitude[magnitude == 0] = 1e-30
    u_norm = dlogN_dt / magnitude
    v_norm = dlogQ_dt / magnitude
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.streamplot(logN_vals, logQ_vals, u_norm, v_norm, density=1.5, color='b', linewidth=0.8)
    N_line = np.logspace(-2, 6, 200)
    Q_null = N_line**(1.5) / gamma_val
    ax1.plot(np.log10(N_line), np.log10(Q_null), 'r--', linewidth=2, label='dN/dt=0 Nullcline')
    ax1.plot(np.log10(N_line), np.log10(N_line), 'g:', linewidth=2, label='Q_mem = N')
    ax1.plot(np.log10(gamma_val**2), np.log10(gamma_val**2), 'ko', markersize=8, label='Quasi-stationary state')
    ax1.set_xlabel('log10(N) (Dimensionless)')
    ax1.set_ylabel('log10(Q_mem) (Dimensionless)')
    ax1.set_title('Phase-Space Streamplot (gamma=' + str(gamma_val) + ', N_s=' + str(Ns_val) + ')')
    ax1.set_xlim(-2, 6)
    ax1.set_ylim(-2, 6)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    t_span = (0, 1e4)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    N0_list = [1e2, 1e3, 1e4]
    for i, N0 in enumerate(N0_list):
        sol = solve_ivp(system, t_span, [N0, 1e-2], method='RK45', events=stop_event, max_step=10)
        label_N = 'N(t), N0=10^' + str(int(np.log10(N0)))
        label_Q = 'Q_mem(t), N0=10^' + str(int(np.log10(N0)))
        ax2.plot(sol.t, sol.y[0], color=colors[i], linestyle='-', linewidth=2, label=label_N)
        ax2.plot(sol.t, sol.y[1], color=colors[i], linestyle='--', linewidth=2, label=label_Q)
    ax2.set_yscale('log')
    ax2.set_xlabel('Time t (Planck units)')
    ax2.set_ylabel('Occupation Number N, Memory Load Q_mem')
    ax2.set_title('Time-Series Trajectories')
    ax2.legend(fontsize=9, loc='best')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    timestamp = int(time.time())
    filename = 'data/phase_space_analysis_1_' + str(timestamp) + '.png'
    plt.savefig(filename, dpi=300)
    print('Plot saved to ' + filename)