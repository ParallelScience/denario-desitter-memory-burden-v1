# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import sympy as sp
import os

def main():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    N, Q, gamma, N_s = sp.symbols('N Q gamma N_s', positive=True)
    H = 1 / sp.sqrt(N)
    dNdt = -H + gamma * Q / N**2
    dQdt = N_s * H
    N_star_expr = gamma**2
    Q_star_expr = gamma**2
    J11 = sp.diff(dNdt, N)
    J12 = sp.diff(dNdt, Q)
    J21 = sp.diff(dQdt, N)
    J22 = sp.diff(dQdt, Q)
    J = sp.Matrix([[J11, J12], [J21, J22]])
    J_star = J.subs({N: N_star_expr, Q: Q_star_expr})
    print('--- Analytical Stability Analysis ---')
    print('Fixed point (N*, Q*) with Q = N:')
    print('N* = ' + str(N_star_expr))
    print('Q* = ' + str(Q_star_expr))
    print('\nJacobian Matrix at fixed point:')
    print('J11 = ' + str(J_star[0, 0]))
    print('J12 = ' + str(J_star[0, 1]))
    print('J21 = ' + str(J_star[1, 0]))
    print('J22 = ' + str(J_star[1, 1]))
    gamma_val = 1e5
    Ns_val = 100.0
    J_num = np.array([[-1.5 * gamma_val**(-3), gamma_val**(-3)], [-0.5 * Ns_val * gamma_val**(-3), 0]], dtype=float)
    eigenvalues = np.linalg.eigvals(J_num)
    print('\nNumerical Eigenvalues for gamma=' + str(gamma_val) + ', N_s=' + str(Ns_val) + ':')
    print('lambda_1 = ' + str(eigenvalues[0]))
    print('lambda_2 = ' + str(eigenvalues[1]))
    N_star = gamma_val**2
    Q_star = gamma_val**2
    H_star = 1.0 / np.sqrt(N_star)
    def simulate(stochastic=False, seed=None):
        if seed is not None:
            np.random.seed(seed)
        t = 0.0
        dt = 1e10
        Y = np.array([N_star, Q_star, 0.0])
        Ns = Ns_val
        history = [[t, Y[0], Y[1], H_star, Y[2], Ns]]
        thresholds = [H_star * (1 - 0.001 * i) for i in range(1, 11)]
        threshold_idx = 0
        while True:
            def F(Y_val, Ns_val):
                N_val, Q_val, Ne_val = Y_val
                H_val = 1.0 / np.sqrt(N_val)
                dN = -H_val + gamma_val * Q_val / (N_val**2)
                dQ = Ns_val * H_val
                dNe = H_val
                return np.array([dN, dQ, dNe])
            k1 = F(Y, Ns)
            k2 = F(Y + 0.5 * dt * k1, Ns)
            k3 = F(Y + 0.5 * dt * k2, Ns)
            k4 = F(Y + dt * k3, Ns)
            Y_new = Y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            t_new = t + dt
            H_new = 1.0 / np.sqrt(Y_new[0])
            if stochastic and threshold_idx < len(thresholds):
                if H_new < thresholds[threshold_idx]:
                    jump = np.random.randint(-10, 11)
                    Ns = max(1.0, Ns + jump)
                    threshold_idx += 1
            Y = Y_new
            t = t_new
            history.append([t, Y[0], Y[1], H_new, Y[2], Ns])
            if abs(H_new - H_star) / H_star > 0.01:
                break
            if t > 1e16:
                break
        return np.array(history)
    print('\n--- Numerical Simulation ---')
    print('Running smooth simulation...')
    history_smooth = simulate(stochastic=False)
    Ne_smooth = history_smooth[-1, 4]
    print('Smooth case success metric: ' + str(round(Ne_smooth, 2)) + ' e-folds elapsed before H drifted by >1%.')
    print('\nRunning stochastic simulations...')
    n_stochastic = 5
    histories_stochastic = []
    for i in range(n_stochastic):
        hist = simulate(stochastic=True, seed=42+i)
        histories_stochastic.append(hist)
        Ne_stoc = hist[-1, 4]
        print('Stochastic realization ' + str(i+1) + ' success metric: ' + str(round(Ne_stoc, 2)) + ' e-folds elapsed before H drifted by >1%.')
    save_dict = {'t_smooth': history_smooth[:, 0], 'N_smooth': history_smooth[:, 1], 'Q_smooth': history_smooth[:, 2], 'H_smooth': history_smooth[:, 3], 'Ne_smooth': history_smooth[:, 4], 'Ns_smooth': history_smooth[:, 5]}
    for i, hist in enumerate(histories_stochastic):
        save_dict['t_stoc_' + str(i)] = hist[:, 0]
        save_dict['N_stoc_' + str(i)] = hist[:, 1]
        save_dict['Q_stoc_' + str(i)] = hist[:, 2]
        save_dict['H_stoc_' + str(i)] = hist[:, 3]
        save_dict['Ne_stoc_' + str(i)] = hist[:, 4]
        save_dict['Ns_stoc_' + str(i)] = hist[:, 5]
    filepath = os.path.join(data_dir, 'step_2_time_series.npz')
    np.savez_compressed(filepath, **save_dict)
    print('\nTime series data saved to ' + filepath)

if __name__ == '__main__':
    main()