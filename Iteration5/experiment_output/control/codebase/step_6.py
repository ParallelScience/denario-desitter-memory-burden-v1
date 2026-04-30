# filename: codebase/step_6.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def plot_phase_diagram():
    data_dir = 'data'
    csv_path = os.path.join(data_dir, 'dynamical_selection_reheating.csv')
    if not os.path.exists(csv_path):
        print('Error: Data file ' + csv_path + ' not found.')
        return
    df = pd.read_csv(csv_path)
    plt.rcParams['text.usetex'] = False
    fig, ax = plt.subplots(figsize=(12, 8))
    H_vals = np.logspace(-8, 0, 1000)
    Ns_cutoff = 1.0 / H_vals**2
    Ns_Ne60 = 1.0 / (60 * H_vals**2)
    Ns_Ne100 = 1.0 / (100 * H_vals**2)
    Ns_Ne1000 = 1.0 / (1000 * H_vals**2)
    ax.plot(H_vals, Ns_cutoff, 'k-', linewidth=2, label='Species Cutoff (N_s = 1/H^2)')
    ax.plot(H_vals, Ns_Ne60, 'r--', linewidth=1.5, label='e-folds N_e = 60')
    ax.plot(H_vals, Ns_Ne100, color='orange', linestyle='--', linewidth=1.5, label='e-folds N_e = 100')
    ax.plot(H_vals, Ns_Ne1000, color='y', linestyle='--', linewidth=1.5, label='e-folds N_e = 1000')
    ax.fill_between(H_vals, Ns_cutoff, 1e15, color='gray', alpha=0.3, label='Forbidden (Species Cutoff)')
    ax.fill_between(H_vals, Ns_Ne60, Ns_cutoff, color='red', alpha=0.15, label='Forbidden (N_e < 60)')
    f_types = df['F_type'].unique()
    colors = {'constant': 'blue', 'logarithmic': 'purple', 'linear': 'cyan'}
    linestyles = {'constant': ':', 'logarithmic': '-.', 'linear': '--'}
    for f_type in f_types:
        subset = df[df['F_type'] == f_type]
        subset = subset.sort_values('H')
        ax.plot(subset['H'], subset['N_s'], color=colors.get(f_type, 'blue'), linestyle=linestyles.get(f_type, '-'), linewidth=3, label='Dynamical Selection: F(x) = ' + str(f_type))
    const_factor = (90.0 / np.pi**2)**0.25 * 1.22e19
    Trh_levels = [1e9, 1e11, 1e13]
    for Trh in Trh_levels:
        Ns_Trh = const_factor / Trh
        ax.axhline(Ns_Trh, color='green', linestyle=':', alpha=0.6)
        ax.text(1e-7, Ns_Trh * 1.2, 'T_rh = 10^' + str(int(np.log10(Trh))) + ' GeV', color='green', fontsize=10)
    ax.axvspan(1e-5, 1e-4, color='blue', alpha=0.1, label='Observational H band (10^-5 - 10^-4)')
    Trh_10MeV_Ns = const_factor / 0.01
    text_str = 'Note: T_rh > 10 MeV is satisfied everywhere\nin the plotted region (requires N_s < ' + '%.1e' % Trh_10MeV_Ns + ')'
    ax.text(0.02, 0.98, text_str, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-8, 1e0)
    ax.set_ylim(1e0, 1e12)
    ax.set_xlabel('Hubble Scale H/M_Pl', fontsize=14)
    ax.set_ylabel('Number of Species N_s', fontsize=14)
    ax.set_title('Observational Viability Phase Diagram', fontsize=16)
    ax.grid(True, which='both', ls='--', alpha=0.5)
    ax.legend(loc='lower left', fontsize=10, ncol=2)
    plt.tight_layout()
    timestamp = int(time.time())
    filepath = os.path.join(data_dir, 'phase_diagram_6_' + str(timestamp) + '.png')
    plt.savefig(filepath, dpi=300)
    plt.close()
    print('Phase diagram saved to ' + filepath)
    print('\n--- Phase Diagram Summary ---')
    print('Constraints plotted:')
    print('  - Species Cutoff: N_s = 1/H^2')
    print('  - e-fold requirements: N_e = 60, 100, 1000')
    print('Dynamical Selection Curves:')
    for f_type in f_types:
        print('  - F(x) = ' + str(f_type))
    print('Reheating Temperature Contours:')
    for Trh in Trh_levels:
        Ns_Trh = const_factor / Trh
        print('  - T_rh = 10^' + str(int(np.log10(Trh))) + ' GeV corresponds to N_s = ' + '%.2e' % Ns_Trh)
    print('\nNote: T_rh > 10 MeV requires N_s < ' + '%.2e' % Trh_10MeV_Ns + ', which is satisfied everywhere in the plotted region.')
    print('Observational Band: H/M_Pl in [1e-5, 1e-4]')

if __name__ == '__main__':
    plot_phase_diagram()