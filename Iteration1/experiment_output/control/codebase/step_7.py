# filename: codebase/step_7.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
sys.path.insert(0, "/home/node/data/compsep_data/")
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from datetime import datetime

plt.rcParams['text.usetex'] = False

def to_sci(val):
    if val == 0:
        return '0.00e0'
    exponent = int(np.floor(np.log10(np.abs(val))))
    mantissa = val / (10**exponent)
    return str(round(mantissa, 2)) + 'e' + str(exponent)

def main():
    data_dir = 'data/'
    
    N_s_vals = np.logspace(0, 8, 1000)
    H_models = {}
    
    H_models['Constant (F=1)'] = N_s_vals**(-0.5)
    
    H_log = np.zeros_like(N_s_vals)
    for i in range(len(N_s_vals)):
        Ns = N_s_vals[i]
        if Ns < 2 * np.e:
            H_log[i] = np.nan
        else:
            def f(x, Ns_val=Ns):
                return np.log(x) / x**2 - 1.0 / Ns_val
            if f(np.sqrt(np.e)) <= 0:
                H_log[i] = np.nan
                continue
            x_high = 10.0
            while f(x_high) > 0:
                x_high *= 10.0
            sol = root_scalar(f, bracket=[np.sqrt(np.e), x_high], method='brentq')
            H_log[i] = 1.0 / sol.root if sol.converged else np.nan
            
    H_models['Logarithmic (F=ln(x))'] = H_log
    H_models['Power-Law (alpha=0.5)'] = N_s_vals**(-2.0/3.0)
    H_models['Power-Law (alpha=1.0)'] = N_s_vals**(-1.0)
    
    print('=== Numerical Verification of Dynamical Selection Equation ===')
    print('Checking constraint: N_s * F(M_Pl/H) = (M_Pl/H)^2')
    
    def verify_model(name, H_vals, F_func):
        valid_idx = ~np.isnan(H_vals)
        Ns_valid = N_s_vals[valid_idx]
        H_valid = H_vals[valid_idx]
        x_valid = 1.0 / H_valid
        LHS = Ns_valid * F_func(x_valid)
        RHS = x_valid**2
        rel_error = np.abs(LHS - RHS) / RHS
        max_error = np.max(rel_error)
        status = 'PASSED' if max_error < 1e-6 else 'FAILED'
        print('Model: ' + name)
        print('  Max relative error: ' + str(max_error))
        print('  Verification: ' + status)
        
    verify_model('Constant (F=1)', H_models['Constant (F=1)'], lambda x: np.ones_like(x))
    verify_model('Logarithmic (F=ln(x))', H_models['Logarithmic (F=ln(x))'], lambda x: np.log(x))
    verify_model('Power-Law (alpha=0.5)', H_models['Power-Law (alpha=0.5)'], lambda x: x**0.5)
    verify_model('Power-Law (alpha=1.0)', H_models['Power-Law (alpha=1.0)'], lambda x: x**1.0)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    linestyles = ['-', '--', '-.', ':']
    model_names = list(H_models.keys())
    for i in range(len(model_names)):
        name = model_names[i]
        H_vals = H_models[name]
        ax.plot(N_s_vals, H_vals, label=name, color=colors[i], linestyle=linestyles[i], linewidth=2.5)
        
    ax.axhspan(1e-5, 1e-4, color='yellow', alpha=0.3, label='Observed Scale (10^-5 <= H/M_Pl <= 10^-4)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1, 1e8)
    ax.set_ylim(1e-9, 1)
    ax.set_xlabel('Number of Species N_s', fontsize=14)
    ax.set_ylabel('Equilibrium Hubble Parameter H/M_Pl', fontsize=14)
    ax.set_title('Dynamical Selection of the Inflationary Scale', fontsize=16)
    ax.grid(True, which='both', ls='--', alpha=0.5)
    ax.legend(loc='upper right', fontsize=12)
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plot_filename = 'dynamical_selection_3_' + timestamp + '.png'
    plot_filepath = os.path.join(data_dir, plot_filename)
    fig.savefig(plot_filepath, dpi=300)
    print('\nPlot saved to ' + plot_filepath)
    
    print('\n=== Assessment of Natural Selection of Inflationary Scale ===')
    for name in model_names:
        H_vals = H_models[name]
        valid_idx = ~np.isnan(H_vals)
        Ns_valid = N_s_vals[valid_idx]
        H_valid = H_vals[valid_idx]
        in_range = (H_valid >= 1e-5) & (H_valid <= 1e-4)
        if np.any(in_range):
            Ns_min = np.min(Ns_valid[in_range])
            Ns_max = np.max(Ns_valid[in_range])
            print('Model ' + name + ' selects the observed scale for N_s between ~' + to_sci(Ns_min) + ' and ~' + to_sci(Ns_max))
        else:
            print('Model ' + name + ' does not select the observed scale within the considered N_s range (1 to 10^8).')

if __name__ == '__main__':
    main()