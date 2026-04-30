# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time

mpl.rcParams['text.usetex'] = False

def ode(t, y, gamma, Ns):
    N, Q = y
    if N < 1e-10:
        return [0.0, 0.0]
    H = N**(-0.5)
    dN = -H + gamma * Q / (N**2)
    dQ = Ns * H
    return [dN, dQ]

def qb_event(t, y, gamma, Ns):
    N, Q = y
    return Q - N
qb_event.terminal = True
qb_event.direction = 1

def min_N_event(t, y, gamma, Ns):
    N, Q = y
    if N < 1e-10:
        return 0.0
    H = N**(-0.5)
    return -H + gamma * Q / (N**2)
min_N_event.terminal = False
min_N_event.direction = 1

def main():
    H0 = 1e-4
    N0 = 1.0 / (H0**2)
    cases = [(1e5, 100), (1e5, 10), (1e6, 100)]
    results = []
    print("==================================================================")
    print(" Formalization and Simulation of the Dynamical Feedback System")
    print("==================================================================\n")
    print("Initial conditions: H_0 = " + ("%.1e" % H0) + ", N_0 = " + ("%.1e" % N0) + ", Q_mem(0) = 0.0\n")
    for gamma, Ns in cases:
        print("--- Simulating case: gamma = " + ("%.1e" % gamma) + ", N_s = " + str(Ns) + " ---")
        Q_star_initial = (N0**1.5) / gamma
        print("Analytical fixed-point condition Q_mem^* (at N_0) = " + ("%.3e" % Q_star_initial))
        y0 = [N0, 0.0]
        t_span = (0, 1e14)
        sol = solve_ivp(ode, t_span, y0, args=(gamma, Ns), events=[qb_event, min_N_event], rtol=1e-10, atol=1e-10, max_step=1e10, dense_output=True)
        t_events = sol.t_events
        y_events = sol.y_events
        if len(t_events[1]) > 0:
            t_stab = t_events[1][0]
            N_stab = y_events[1][0][0]
            Q_stab = y_events[1][0][1]
            Q_star_analytical = (N_stab**1.5) / gamma
            print("Stabilization (dN/dt = 0) reached at t = " + ("%.3e" % t_stab))
            print("Analytical Q_mem^* (at stabilization N) = " + ("%.3e" % Q_star_analytical))
            print("Numerically observed Q_mem at stabilization = " + ("%.3e" % Q_stab))
            print("Consistency check (Numerical / Analytical) = " + ("%.5f" % (Q_stab / Q_star_analytical)))
        else:
            print("Stabilization event not reached.")
        if len(t_events[0]) > 0:
            t_qb = t_events[0][0]
            print("Onset of quantum breaking identified at t_qb = " + ("%.3e" % t_qb))
        else:
            print("Quantum breaking event not reached.")
            t_qb = sol.t[-1]
        print("Time evolution of Q_mem(t) / N(t):")
        for frac in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
            t_eval = frac * t_qb
            y_eval = sol.sol(t_eval)
            ratio_eval = y_eval[1] / y_eval[0]
            print("  At t = " + ("%.3e" % t_eval) + " (" + str(int(frac*100)) + "% of t_qb): Q_mem/N = " + ("%.5e" % ratio_eval))
        print("\n")
        t_plot = np.linspace(0, t_qb, 2000)
        y_plot = sol.sol(t_plot)
        N_plot = y_plot[0]
        Q_plot = y_plot[1]
        H_plot = N_plot**(-0.5)
        ratio_plot = Q_plot / N_plot
        results.append({'gamma': gamma, 'Ns': Ns, 't': t_plot, 'N': N_plot, 'H': H_plot, 'Q': Q_plot, 'ratio': ratio_plot})
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    for res in results:
        label = "gamma=" + ("%.0e" % res['gamma']) + ", N_s=" + str(res['Ns'])
        axs[0, 0].plot(res['t'], res['N'], label=label, linewidth=2)
        axs[0, 1].plot(res['t'], res['H'], label=label, linewidth=2)
        axs[1, 0].plot(res['t'], res['Q'], label=label, linewidth=2)
        axs[1, 1].plot(res['t'], res['ratio'], label=label, linewidth=2)
    axs[0, 0].set_title("Graviton Occupation Number N(t)", fontsize=14)
    axs[0, 0].set_xlabel("Time t [M_Pl^-1]", fontsize=12)
    axs[0, 0].set_ylabel("N", fontsize=12)
    axs[0, 0].grid(True, alpha=0.6)
    axs[0, 0].legend(fontsize=10)
    axs[0, 1].set_title("Hubble Parameter H(t)", fontsize=14)
    axs[0, 1].set_xlabel("Time t [M_Pl^-1]", fontsize=12)
    axs[0, 1].set_ylabel("H [M_Pl]", fontsize=12)
    axs[0, 1].grid(True, alpha=0.6)
    axs[0, 1].legend(fontsize=10)
    axs[1, 0].set_title("Memory Load Q_mem(t)", fontsize=14)
    axs[1, 0].set_xlabel("Time t [M_Pl^-1]", fontsize=12)
    axs[1, 0].set_ylabel("Q_mem", fontsize=12)
    axs[1, 0].grid(True, alpha=0.6)
    axs[1, 0].legend(fontsize=10)
    axs[1, 1].set_title("Ratio Q_mem(t) / N(t)", fontsize=14)
    axs[1, 1].set_xlabel("Time t [M_Pl^-1]", fontsize=12)
    axs[1, 1].set_ylabel("Q_mem / N", fontsize=12)
    axs[1, 1].axhline(1.0, color='r', linestyle='--', label="Quantum Breaking (Q_mem=N)")
    axs[1, 1].grid(True, alpha=0.6)
    axs[1, 1].legend(fontsize=10)
    plt.tight_layout()
    timestamp = int(time.time())
    filepath = "data/dynamical_feedback_simulation_1_" + str(timestamp) + ".png"
    plt.savefig(filepath, dpi=300)
    print("Plot saved to " + filepath)

if __name__ == '__main__':
    main()