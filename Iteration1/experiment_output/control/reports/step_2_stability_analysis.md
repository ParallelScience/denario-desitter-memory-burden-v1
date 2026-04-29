<!-- filename: reports/step_2_stability_analysis.md -->
# Stability Analysis of the Feedback System

## 1. Updated Feedback Equation and Fixed-Point Condition
The evolution of the graviton occupation number $N$ is governed by the competition between the natural depletion of the condensate and the stabilizing backreaction from the memory burden $Q_{mem}$. The feedback equation is given by:

$dN/dt = -H + \gamma(N) \frac{Q_{mem}}{N^2}$

where $H = M_{Pl}/\sqrt{N}$ is the Hubble parameter. To account for the collective coupling of the graviton condensate, we update the feedback coupling to scale as $\gamma(N) = \gamma_0 / N$, where $\gamma_0$ is an order-one constant. Substituting this into the evolution equation yields:

$dN/dt = -H + \gamma_0 \frac{Q_{mem}}{N^3} = -N^{-1/2} + \gamma_0 \frac{Q_{mem}}{N^3}$ 

(working in Planck units $M_{Pl} = 1$).

The system reaches a metastable quasi-de Sitter state when the depletion is exactly counteracted by the memory burden, i.e., $dN/dt = 0$. This yields the analytical fixed-point condition (representing the slow manifold of the system):

$Q_{mem}^* = \frac{N^3 H}{\gamma_0} = \frac{N^{5/2}}{\gamma_0}$

## 2. Linear Stability Analysis and Jacobian
To classify the stability of this metastable state, we analyze the coupled 2D dynamical system for $N$ and $Q_{mem}$. The memory accumulation rate is given by $dQ_{mem}/dt = N_s H$. Thus, the full system is:

$f(N, Q_{mem}) = \frac{dN}{dt} = -N^{-1/2} + \gamma_0 Q_{mem} N^{-3}$

$g(N, Q_{mem}) = \frac{dQ_{mem}}{dt} = N_s N^{-1/2}$

We compute the Jacobian matrix $J$ evaluated at the slow manifold $Q_{mem}^* = N^{5/2} / \gamma_0$:

$J = \begin{pmatrix} \frac{\partial f}{\partial N} & \frac{\partial f}{\partial Q_{mem}} \\ \frac{\partial g}{\partial N} & \frac{\partial g}{\partial Q_{mem}} \end{pmatrix}$

Evaluating the partial derivatives at $Q_{mem}^*$:
- $J_{11} = \frac{1}{2}N^{-3/2} - 3\gamma_0 Q_{mem}^* N^{-4} = \frac{1}{2}N^{-3/2} - 3N^{-3/2} = -2.5 N^{-3/2}$
- $J_{12} = \gamma_0 N^{-3}$
- $J_{21} = -\frac{1}{2} N_s N^{-3/2}$
- $J_{22} = 0$

Thus, the Jacobian at the metastable state is:

$J = \begin{pmatrix} -2.5 N^{-3/2} & \gamma_0 N^{-3} \\ -0.5 N_s N^{-3/2} & 0 \end{pmatrix}$

## 3. Eigenvalues and Classification
To classify the fixed point, we compute the trace ($\tau$) and determinant ($\Delta$) of the Jacobian:
- **Trace:** $\tau = Tr(J) = -2.5 N^{-3/2}$
- **Determinant:** $\Delta = Det(J) = - (\gamma_0 N^{-3})(-0.5 N_s N^{-3/2}) = 0.5 \gamma_0 N_s N^{-9/2}$

The eigenvalues $\lambda$ are given by the characteristic equation $\lambda^2 - \tau \lambda + \Delta = 0$:

$\lambda_{\pm} = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2}$

The discriminant is:

$\tau^2 - 4\Delta = 6.25 N^{-3} - 2 \gamma_0 N_s N^{-9/2}$

Because both $\tau < 0$ and $\Delta > 0$, the real parts of the eigenvalues are strictly negative for all physical values of $N$ and $N_s$. This conclusively demonstrates that the memory burden provides a robust stabilizing feedback mechanism. 

Depending on the specific parameter regime, the classification is as follows:
- **Stable Node (Primary Regime):** For the vast majority of the physically relevant inflationary parameter space (e.g., $H \sim 10^{-5}$, $N \sim 10^{10}$), the term $N^{-3}$ overwhelmingly dominates over $N^{-9/2}$. The discriminant is strictly positive, making the fixed point a **Stable Node**. The system exhibits a fast relaxation mode ($\lambda_- \approx -2.5 N^{-3/2}$) and a slow drift mode ($\lambda_+ \approx -0.2 \gamma_0 N_s N^{-3}$).
- **Stable Spiral (Extreme Regime):** In extreme corners of the parameter space with a very large number of species ($N_s \sim 10^8$) and high curvature ($H \sim 10^{-2}$, $N \sim 10^4$), the discriminant can become negative (specifically when $N^{3/2} < 0.32 \gamma_0 N_s$). Here, the fixed point transitions into a **Stable Spiral**, where the system exhibits damped oscillations as it settles onto the slow manifold. 

In both cases, the real part of the eigenvalues remains strictly negative, ensuring robust stability.

## 4. Investigation of Limit Cycles and Quasi-de Sitter Dynamics
We investigated whether the $1/N$ dependence in the feedback coupling could lead to a limit cycle (e.g., via a Hopf bifurcation), which might provide an alternative dynamical explanation for the quasi-de Sitter phase. 

A limit cycle emerging from a fixed point requires a Hopf bifurcation, which occurs when the trace of the Jacobian crosses zero ($\tau = 0$) while the determinant remains positive. However, our analysis shows that $\tau = -2.5 N^{-3/2}$ is strictly negative for all physical values of $N > 0$. Consequently, **no Hopf bifurcation occurs, and the system does not exhibit a limit cycle.**

Instead, the dynamical explanation for the quasi-de Sitter expansion lies in the **slow-fast dynamics** of the stable node. The large separation of timescales between the fast eigenvalue ($\lambda_-$) and the slow eigenvalue ($\lambda_+$) means the system rapidly collapses onto the slow manifold ($dN/dt \approx 0$) and becomes locked there. As $Q_{mem}$ slowly accumulates, $N$ (and therefore $H$) evolves adiabatically. This strong attractor behavior dynamically generates a prolonged quasi-de Sitter phase with $H \approx \text{const}$ without requiring a fundamental cosmological constant.

## 5. Instructions for Numerical Implementation (Step 3)
For the engineer executing Step 3, please use the following concrete analytical results:
1. **Initial Conditions:** To simulate the quasi-de Sitter plateau efficiently and avoid initial transient oscillations, initialize the system exactly on the slow manifold. For a chosen initial $N_0$, set the initial memory load to:
   $Q_{mem}(0) = \frac{N_0^3 H_0}{\gamma_0} = \frac{N_0^{5/2}}{\gamma_0}$
2. **System of ODEs:** Implement the coupled system:
   $dN/dt = -N^{-1/2} + \gamma_0 Q_{mem} N^{-3}$
   $dQ_{mem}/dt = N_s N^{-1/2}$
   (Set $\gamma_0 = 1$ for simplicity unless otherwise specified).
3. **Attractor Verification:** The analytical classification as a **Stable Node** guarantees that small perturbations away from $Q_{mem}(0)$ will rapidly decay back to the manifold. You can verify this numerically by slightly offsetting the initial $Q_{mem}$ and observing the fast relaxation.