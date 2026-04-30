# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
import time
import os

def main():
    data_path = "data/inflationary_grid_3_1777543491.npz"
    if not os.path.exists(data_path):
        print("Error: Data file not found at " + data_path)
        return
    data = np.load(data_path)
    H_grid = data['H_init']
    Ns_grid = data['Ns']
    Ne_grid = data['Ne']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    Ne_safe = np.where(Ne_grid > 0, Ne_grid, 1e-10)
    log_Ne = np.log10(Ne_safe)
    cf = ax1.contourf(Ns_grid, H_grid, log_Ne, levels=50, cmap='viridis')
    cbar = fig.colorbar(cf, ax=ax1)
    cbar.set_label('log10(N_e)')
    ax1.contour(Ns_grid, H_grid, Ne_grid, levels=[60], colors='red', linewidths=3)
    ax1.plot([], [], color='red', linewidth=3, label='N_e = 60 (Stability Corridor)')
    H_curve = np.logspace(-5, -2, 200)
    Ns_cutoff = 1.0 / H_curve**2
    ax1.plot(Ns_cutoff, H_curve, 'w--', linewidth=2, label='Species Cutoff / F(x)=1: N_s = 1/H^2')
    Ns_efold = 1.0 / (60.0 * H_curve**2)
    ax1.plot(Ns_efold, H_curve, 'w:', linewidth=2, label='E-fold Req: N_s = 1/(60 H^2)')
    Ns_dyn_log = 1.0 / (H_curve**2 * np.log(1.0 / H_curve))
    ax1.plot(Ns_dyn_log, H_curve, 'c-.', linewidth=2, label='Dyn. Sel. F(x)=log(x)')
    Ns_dyn_sqrt = 1.0 / (H_curve**1.5)
    ax1.plot(Ns_dyn_sqrt, H_curve, 'm-.', linewidth=2, label='Dyn. Sel. F(x)=x^0.5')
    ax1.axhspan(1e-5, 1e-4, color='gray', alpha=0.3, label='CMB Window (10^-5 - 10^-4)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(np.min(Ns_grid), np.max(Ns_grid))
    ax1.set_ylim(np.min(H_grid), np.max(H_grid))
    ax1.set_xlabel('Number of Species N_s')
    ax1.set_ylabel('Initial Hubble Scale H_init / M_Pl')
    ax1.set_title('Phase Diagram of Inflationary E-folds')
    ax1.legend(loc='upper right', fontsize=8)
    target_H = [1e-5, 1e-4, 1e-3]
    colors = ['blue', 'green', 'purple']
    for H_val, color in zip(target_H, colors):
        idx = np.argmin(np.abs(H_grid[:, 0] - H_val))
        actual_H = H_grid[idx, 0]
        Ns_vals = Ns_grid[idx, :]
        Ne_num = Ne_grid[idx, :]
        Ne_ana = 1.0 / (Ns_vals * actual_H**2)
        H_label = "%.1e" % actual_H
        ax2.plot(Ns_vals, Ne_num, 'o', color=color, markersize=5, label='Num. H ~ ' + H_label)
        ax2.plot(Ns_vals, Ne_ana, '-', color=color, linewidth=2, label='Ana. H ~ ' + H_label)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Number of Species N_s')
    ax2.set_ylabel('Number of E-folds N_e')
    ax2.set_title('E-folds vs Species Count for Fixed H')
    ax2.legend(loc='lower left', fontsize=9)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    timestamp = int(time.time())
    filename = "data/observational_viability_4_" + str(timestamp) + ".png"
    plt.savefig(filename, dpi=300)
    print("Plot saved to " + filename)
    print("\n=== Observational Viability Summary ===")
    print("Data loaded from: " + data_path)
    print("Grid dimensions: " + str(H_grid.shape))
    print("H_init range: " + ("%.1e" % np.min(H_grid)) + " to " + ("%.1e" % np.max(H_grid)))
    print("N_s range: " + ("%.1e" % np.min(Ns_grid)) + " to " + ("%.1e" % np.max(Ns_grid)))
    print("N_e range: " + ("%.1e" % np.min(Ne_grid)) + " to " + ("%.1e" % np.max(Ne_grid)))
    valid_points = np.sum(Ne_grid >= 60)
    total_points = Ne_grid.size
    print("Points in stability corridor (N_e >= 60): " + str(valid_points) + " out of " + str(total_points))
    cmb_mask = (H_grid >= 1e-5) & (H_grid <= 1e-4)
    cmb_valid = np.sum((Ne_grid >= 60) & cmb_mask)
    print("Points in CMB window with N_e >= 60: " + str(cmb_valid))

if __name__ == '__main__':
    main()