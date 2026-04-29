# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import time

def calculate_fixed_point(gamma, H):
    return np.sqrt(gamma / H)

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = "data"
    H = 1e-2
    gamma_example = 1e6
    print("--- Fixed Point Analysis ---")
    print("Parameters: H = " + str(H) + ", gamma = " + str(gamma_example))
    print("Fixed point calculation specified as:")
    print("N* = (gamma * Q_mem / H)^(1/3) evaluated at Q_mem = N*")
    print("=> N* = sqrt(gamma / H)")
    N_star = calculate_fixed_point(gamma_example, H)
    Q_mem_star = N_star
    print("N* = %.4e" % N_star)
    print("Q_mem* = %.4e" % Q_mem_star)
    J = np.array([
        [-2 * gamma_example * Q_mem_star / N_star**3, gamma_example / N_star**2],
        [0, 0]
    ])
    eigenvalues = np.linalg.eigvals(J)
    print("\nJacobian at fixed point:")
    print("[[%.4e, %.4e]" % (J[0,0], J[0,1]))
    print(" [%.4e, %.4e]]" % (J[1,0], J[1,1]))
    print("Eigenvalues: %.4e, %.4e" % (eigenvalues[0], eigenvalues[1]))
    print("Stability: The non-zero negative eigenvalue indicates stability in the N-direction.")
    print("The zero eigenvalue corresponds to the constant drift in Q_mem (dQ_mem/dt = const).")
    gamma_vals = [1e6, 5e6]
    Ns_vals = [100, 1000]
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    results = {}
    for i, gamma in enumerate(gamma_vals):
        for j, N_s in enumerate(Ns_vals):
            ax = axes[i, j]
            N_grid_vals = np.linspace(100, 30000, 200)
            Q_grid_vals = np.linspace(0, 40000, 200)
            N_grid, Q_grid = np.meshgrid(N_grid_vals, Q_grid_vals)
            dN_grid = -H + gamma * Q_grid / N_grid**2
            dQ_grid = np.ones_like(N_grid) * N_s * H
            norm = np.sqrt(dN_grid**2 + dQ_grid**2)
            norm[norm == 0] = 1e-10
            ax.streamplot(N_grid_vals, Q_grid_vals, dN_grid/norm, dQ_grid/norm, color='lightgray', linewidth=0.8, density=1.2)
            N_null = np.linspace(100, 30000, 500)
            Q_null = H * N_null**3 / gamma
            ax.plot(N_null, Q_null, 'k--', linewidth=2, label='Nullcline dN/dt = 0')
            ax.plot(N_null, N_null, 'r:', linewidth=2, label='Quantum Breaking (Q_mem = N)')
            N_star_plot = np.sqrt(gamma / H)
            ax.plot(N_star_plot, N_star_plot, 'go', markersize=8, label='Fixed Point N*')
            N0_vals = [5000, 10000, 15000, 20000, 25000]
            t_end = 40000 / (N_s * H)
            t_span = (0, t_end)
            t_eval = np.linspace(0, t_end, 1000)
            traj_data = []
            for N0 in N0_vals:
                sol = solve_ivp(lambda t, y, g=gamma, ns=N_s: [-H + g * y[1] / y[0]**2, ns * H], t_span, [N0, 0.0], t_eval=t_eval, method='Radau')
                ax.plot(sol.y[0], sol.y[1], linewidth=2, label='Traj N0=' + str(N0))
                traj_data.append({'N0': N0, 't': sol.t, 'N': sol.y[0], 'Q_mem': sol.y[1]})
            ax.set_title('gamma = ' + ("%.1e" % gamma) + ', N_s = ' + str(N_s), fontsize=14)
            ax.set_xlabel('Graviton Number N', fontsize=12)
            ax.set_ylabel('Memory Load Q_mem', fontsize=12)
            ax.set_xlim(0, 30000)
            ax.set_ylim(0, 40000)
            ax.grid(True, alpha=0.3)
            if i == 0 and j == 0:
                ax.legend(loc='upper left', fontsize=9)
            key = 'gamma_' + str(gamma) + '_Ns_' + str(N_s)
            results[key] = traj_data
    plt.tight_layout()
    timestamp = int(time.time())
    plot_filename = os.path.join(data_dir, "phase_portraits_2_" + str(timestamp) + ".png")
    plt.savefig(plot_filename, dpi=300)
    print("\nPhase portraits saved to " + plot_filename)
    data_filename = os.path.join(data_dir, "stability_data.npz")
    save_dict = {'gamma_vals': np.array(gamma_vals), 'Ns_vals': np.array(Ns_vals), 'H': np.array([H])}
    for key, trajs in results.items():
        for idx, traj in enumerate(trajs):
            save_dict[key + "_traj_" + str(idx) + "_t"] = traj['t']
            save_dict[key + "_traj_" + str(idx) + "_N"] = traj['N']
            save_dict[key + "_traj_" + str(idx) + "_Q_mem"] = traj['Q_mem']
    np.savez_compressed(data_filename, **save_dict)
    print("Numerical results saved to " + data_filename)

if __name__ == '__main__':
    main()