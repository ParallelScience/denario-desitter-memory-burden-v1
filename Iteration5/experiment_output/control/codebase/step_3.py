# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import time
import os

def plot_perturbation_spectrum():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    plt.rcParams['text.usetex'] = False
    csv_path = 'data/perturbation_spectrum.csv'
    if not os.path.exists(csv_path):
        print('Error: Data file ' + csv_path + ' not found.')
        return
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['n_s', 'r'])
    df_plot = df[(df['n_s'] > 0.8) & (df['n_s'] < 1.2) & (df['r'] >= -0.01) & (df['r'] < 0.5)].copy()
    if len(df_plot) == 0:
        print('No data points in the specified range to plot.')
        return
    fig, ax = plt.subplots(figsize=(10, 8))
    ellipse_95 = Ellipse(xy=(0.9649, 0.028), width=0.0168, height=0.056, edgecolor='blue', fc='blue', alpha=0.2, label='Planck 2018 (95% CL)')
    ellipse_68 = Ellipse(xy=(0.9649, 0.014), width=0.0084, height=0.028, edgecolor='blue', fc='blue', alpha=0.4, label='Planck 2018 (68% CL)')
    ax.add_patch(ellipse_95)
    ax.add_patch(ellipse_68)
    sc = ax.scatter(df_plot['n_s'], df_plot['r'], c=np.log10(df_plot['N_s']), cmap='viridis', s=60, edgecolor='k', zorder=3)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('log10(N_s)', fontsize=14)
    ax.set_xlim(0.92, 1.02)
    ax.set_ylim(-0.01, 0.12)
    ax.set_xlabel('Scalar spectral index n_s', fontsize=14)
    ax.set_ylabel('Tensor-to-scalar ratio r', fontsize=14)
    ax.set_title('Perturbation Spectrum: n_s vs r', fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=12)
    plt.tight_layout()
    timestamp = int(time.time())
    filepath = 'data/perturbation_spectrum_3_' + str(timestamp) + '.png'
    plt.savefig(filepath, dpi=300)
    plt.close()
    print('Plot saved to ' + filepath)
    print('\n--- Perturbation Spectrum Analysis ---')
    print('Total valid points in plot range: ' + str(len(df_plot)))
    in_95 = df_plot[((df_plot['n_s'] - 0.9649)/(0.0168/2))**2 + ((df_plot['r'] - 0.028)/(0.056/2))**2 <= 1]
    print('Points within 95% CL: ' + str(len(in_95)))
    if len(in_95) > 0:
        print('\nParameters of points within 95% CL:')
        print(in_95[['gamma', 'alpha', 'N_s', 'H0', 'n_s', 'r']].to_string(index=False))
    else:
        print('\nNo points fall strictly within the 95% CL ellipse.')
        df_plot['dist_to_center'] = np.sqrt(((df_plot['n_s'] - 0.9649)/(0.0168/2))**2 + ((df_plot['r'] - 0.028)/(0.056/2))**2)
        closest = df_plot.sort_values('dist_to_center').head(5)
        print('\nClosest 5 points to the Planck 2018 central value:')
        print(closest[['gamma', 'alpha', 'N_s', 'H0', 'n_s', 'r']].to_string(index=False))

if __name__ == '__main__':
    plot_perturbation_spectrum()