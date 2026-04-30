# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import sympy as sp
import os

def main():
    data_dir = 'data'
    N, Q, gamma, Ns = sp.symbols('N Q gamma N_s', positive=True)
    H = 1 / sp.sqrt(N)
    dNdt = -H + gamma * Q / N**2
    dQdt = Ns * H
    dHdt = sp.diff(H, N) * dNdt
    epsilon = -dHdt / H**2
    deps_dt = sp.diff(epsilon, N) * dNdt + sp.diff(epsilon, Q) * dQdt
    eta = deps_dt / (H * epsilon)
    ns = 1 - 6*epsilon + 2*eta
    dns_dt = sp.diff(ns, N) * dNdt + sp.diff(ns, Q) * dQdt
    alphas = dns_dt / H
    Q_attractor = N * (1 + sp.Rational(2, 3) * Ns)
    gamma_val = sp.sqrt(N)
    epsilon_sub = sp.simplify(epsilon.subs(gamma, gamma_val).subs(Q, Q_attractor))
    eta_sub = sp.simplify(eta.subs(gamma, gamma_val).subs(Q, Q_attractor))
    ns_sub = sp.simplify(ns.subs(gamma, gamma_val).subs(Q, Q_attractor))
    alphas_sub = sp.simplify(alphas.subs(gamma, gamma_val).subs(Q, Q_attractor))
    ns_func = sp.lambdify((N, Ns), ns_sub, 'numpy')
    alphas_func = sp.lambdify((N, Ns), alphas_sub, 'numpy')
    Ns_vals = np.logspace(0, 8, 500)
    H_vals = np.logspace(-5, -2, 500)
    Ns_grid, H_grid = np.meshgrid(Ns_vals, H_vals)
    N_grid = 1.0 / H_grid**2
    Trh_Planck = (30.0 / np.pi**2)**0.25 * np.sqrt(H_grid) / (Ns_grid**0.25)
    M_Pl_MeV = 1.22e22
    Trh_MeV = Trh_Planck * M_Pl_MeV
    mask_BBN = Trh_MeV > 10.0
    ns_grid = np.broadcast_to(ns_func(N_grid, Ns_grid), N_grid.shape)
    alphas_grid = np.broadcast_to(alphas_func(N_grid, Ns_grid), N_grid.shape)
    mask_ns_planck = (ns_grid >= 0.961) & (ns_grid <= 0.969)
    mask_species = Ns_grid <= (1.0 / H_grid**2)
    Ne = 60.0
    mask_quantum_breaking = (Ne * Ns_grid) <= (1.0 / H_grid**2)
    mask_all = mask_BBN & mask_quantum_breaking & mask_ns_planck
    filepath = os.path.join(data_dir, 'step_3_parameter_sweep.npz')
    np.savez_compressed(filepath, Ns_grid=Ns_grid, H_grid=H_grid, Trh_MeV=Trh_MeV, ns_grid=ns_grid, alphas_grid=alphas_grid, mask_BBN=mask_BBN, mask_species=mask_species, mask_quantum_breaking=mask_quantum_breaking, mask_ns_planck=mask_ns_planck)
    print('Saved to ' + filepath)

if __name__ == '__main__':
    main()