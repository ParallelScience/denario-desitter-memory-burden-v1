# filename: codebase/step_5.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import pandas as pd

def compute_boundaries_and_r():
    data_dir = 'data/'
    N_s_vals = np.logspace(0, 8, 1000)
    H_species = 1.0 / np.sqrt(N_s_vals)
    Ne_vals = [30, 60, 100]
    H_Ne = {}
    for Ne in Ne_vals:
        H_Ne['H_Ne_' + str(Ne)] = 1.0 / np.sqrt(Ne * N_s_vals)
    df_boundaries = pd.DataFrame({'N_s': N_s_vals, 'H_species_cutoff': H_species})
    for Ne in Ne_vals:
        df_boundaries['H_Ne_' + str(Ne)] = H_Ne['H_Ne_' + str(Ne)]
    boundaries_filepath = os.path.join(data_dir, 'phase_boundaries.csv')
    df_boundaries.to_csv(boundaries_filepath, index=False)
    print('Saved boundaries to ' + boundaries_filepath)
    H_grid_vals = np.logspace(-6, -1, 500)
    N_s_grid, H_grid = np.meshgrid(N_s_vals, H_grid_vals)
    gamma_0 = 1.0
    epsilon_grid = 0.2 * gamma_0 * N_s_grid * (H_grid)**5
    r_grid = 16.0 * epsilon_grid
    grid_filepath = os.path.join(data_dir, 'r_tensor_scalar_grid.npz')
    np.savez(grid_filepath, N_s=N_s_grid, H=H_grid, epsilon=epsilon_grid, r=r_grid)
    print('Saved r grid to ' + grid_filepath)
    print('\n=== Analytical Derivation of Slow-Roll Parameter ===')
    print('1. Definition: epsilon = -dot(H)/H^2')
    print('2. From N = M_Pl^2 / H^2, we have H = M_Pl * N^{-1/2}')
    print('   Therefore, dot(H) = -0.5 * M_Pl * N^{-3/2} * dot(N)')
    print('3. Substituting dot(H): epsilon = 0.5 * (M_Pl * N^{-3/2} * dot(N)) / (M_Pl^2 * N^{-1})')
    print('   epsilon = 0.5 * M_Pl^{-1} * N^{-1/2} * dot(N) = 0.5 * (H / M_Pl^2) * dot(N)')
    print('   Setting M_Pl = 1: epsilon = 0.5 * H * dot(N)')
    print('4. Feedback equation: dot(N) = -H + gamma_0 * Q_mem / N^3')
    print('5. Slow manifold condition: Q_mem = N^{5/2} / gamma_0')
    print('6. Departure from exact fixed point due to memory accumulation (dot(Q_mem) = N_s * H):')
    print('   Taking time derivative of slow manifold: dot(Q_mem) = (5/2) * N^{3/2} * dot(N) / gamma_0')
    print('   Equating to N_s * N^{-1/2}: dot(N) = (2/5) * gamma_0 * N_s * N^{-2}')
    print('7. Final epsilon: epsilon = 0.5 * N^{-1/2} * (2/5 * gamma_0 * N_s * N^{-2}) = 0.2 * gamma_0 * N_s * H^5')
    print('8. Tensor-to-scalar ratio: r = 16 * epsilon = 3.2 * gamma_0 * N_s * H^5')
    print('\n=== Key Numerical Results ===')
    print('For H/M_Pl = 10^-5 and N_s = 100:')
    H_test = 1e-5
    Ns_test = 100
    r_test = 3.2 * gamma_0 * Ns_test * (H_test)**5
    print('r = ' + str(r_test) + ' (Observational bound: r < 0.036)')
    print('\nBoundary values at N_s = 100:')
    print('Species cutoff H: ' + str(1.0 / np.sqrt(100)))
    print('N_e = 30 cutoff H: ' + str(1.0 / np.sqrt(30 * 100)))
    print('N_e = 60 cutoff H: ' + str(1.0 / np.sqrt(60 * 100)))
    print('N_e = 100 cutoff H: ' + str(1.0 / np.sqrt(100 * 100)))

if __name__ == '__main__':
    compute_boundaries_and_r()