<!-- filename: reports/step_1_corpuscular_gravity_notes.md -->
### Foundational Theoretical Derivations

#### 1. Derivation of the Bogoliubov Dispersion Relation and Holographic Scaling

In the corpuscular framework, a Hubble patch of de Sitter spacetime is not a fundamental geometric background but a coherent state (a Bose-Einstein condensate) of $N$ soft gravitons. The characteristic wavelength of these gravitons is the Hubble radius $R_H \sim H^{-1}$, and their occupation number is given by $N = M_{Pl}^2 / H^2$. The collective dimensionless coupling among the gravitons is $\alpha \sim 1/N$, placing the condensate exactly at the quantum critical point $\alpha N \sim 1$.

To understand the information storage capacity of this spacetime, we expand the Hamiltonian of the graviton condensate around its macroscopic ground state. Let $a_0^\dagger$ and $a_0$ be the creation and annihilation operators for the condensate gravitons, such that the expectation value of the number operator is $\langle a_0^\dagger a_0 \rangle = N$. The fluctuations are described by operators $a_k^\dagger$ and $a_k$ for modes with momentum $k > 0$.

The effective Hamiltonian to quadratic order in the fluctuations takes the form:
<code>
\mathcal{H} \approx \mathcal{H}_0(N) + \sum_{k \neq 0} \left[ A_k a_k^\dagger a_k + \frac{1}{2} B_k (a_k^\dagger a_{-k}^\dagger + a_k a_{-k}) \right]
</code>
where the coefficients $A_k$ and $B_k$ depend on the condensate density and the collective coupling $\alpha$. At the quantum critical point $\alpha N = 1$, the system undergoes a Bogoliubov transformation to diagonalize the Hamiltonian:
<code>
b_k = u_k a_k + v_k a_{-k}^\dagger
</code>
where $u_k^2 - v_k^2 = 1$. The diagonalized Hamiltonian becomes $\mathcal{H} \approx \mathcal{H}_0 + \sum_k \epsilon_k b_k^\dagger b_k$.

Because the system is at a quantum critical point, the energy gap for the lowest-lying Bogoliubov modes is extremely suppressed. In terms of the characteristic energy scale of the condensate $H$, the energy of these modes scales as:
<code>
\epsilon_k \sim \frac{H}{N} \sim \frac{H^3}{M_{Pl}^2}
</code>
This near-gapless nature allows these modes to be easily excited, serving as the primary channels for information storage (memory modes). The dispersion relation for these modes can be parameterized as:
<code>
\epsilon_k = H \left( \frac{k}{H} \right)^\delta
</code>
where $\delta$ is a scaling exponent determined by the geometry of the condensate. For a system that respects the holographic principle, the total number of available memory modes must scale with the area of the de Sitter horizon, meaning the maximum entropy is $S_{dS} \sim N \sim M_{Pl}^2/H^2$.

The memory load functional $F(M_{Pl}/H)$ represents the equilibrium phase space volume of these memory modes. If the memory load scales holographically, the functional must be proportional to the number of constituents, $F(M_{Pl}/H) \sim (M_{Pl}/H)^2$. However, depending on the exact nature of the quantum critical point and the dimensionality of the boundary, $F$ could take other forms (e.g., logarithmic or different power laws), which will be systematically explored in subsequent numerical analyses. The scaling of $F$ is fundamentally anchored in the requirement that the density of states integrated up to the species cutoff $\Lambda_g$ reproduces the holographic entropy bound.

#### 2. Formalization of the Quantum Breaking Transition

The semiclassical approximation of gravity relies on treating the metric as a classical background field, governed by the Einstein field equations $G_{\mu\nu} = 8\pi G \langle T_{\mu\nu} \rangle$. This approximation is valid only as long as the quantum fluctuations of the metric are negligible compared to the background energy density. In the corpuscular picture, this translates to the requirement that the backreaction of the memory modes (the Bogoliubov excitations $b_k$) on the condensate is small.

The memory load is quantified by the total occupation number of the excited modes:
<code>
Q_{mem} = \sum_k \langle b_k^\dagger b_k \rangle
</code>
The presence of these modes alters the energy of the condensate. The backreaction energy is given by:
<code>
\Delta E_{mem} \sim \frac{Q_{mem}}{N} (N - N_c)
</code>
where $N_c$ is the critical occupation number. This backreaction modifies the depletion rate of the condensate. The evolution of the graviton occupation number $N$ is governed by the feedback equation:
<code>
\frac{dN}{dt} = -H + \gamma \frac{Q_{mem}}{N^2}
</code>
where the first term represents the standard quantum depletion (Hawking-Gibbons radiation) and the second term represents the stabilizing feedback from the memory burden, with $\gamma$ being an order-one constant.

Memory accumulates due to the continuous production of excitations, which is proportional to the number of available particle species $N_s$ and the Hubble rate:
<code>
\frac{dQ_{mem}}{dt} \sim N_s H
</code>
Assuming an initial state with zero memory load ($Q_{mem}(0) = 0$), the memory load grows linearly with time:
<code>
Q_{mem}(t) \sim N_s H t
</code>
Quantum breaking occurs when the memory burden becomes comparable to the condensate size, $Q_{mem} \sim N$. At this point, the backreaction term $\gamma Q_{mem}/N^2$ dominates, and the semiclassical description of the de Sitter horizon fails because the energy density of the condensate is no longer sufficient to maintain the macroscopic geometry against the pressure of the quantum fluctuations.

The timescale for this transition, the quantum breaking time $t_{qb}$, is found by setting $Q_{mem}(t_{qb}) = N$:
<code>
t_{qb} \sim \frac{N}{N_s H} = \frac{M_{Pl}^2}{N_s H^3}
</code>
At $t = t_{qb}$, the trajectory of the system crosses the critical manifold where the semiclassical approximation breaks down. The failure condition for the de Sitter horizon geometry is thus defined as the saturation of the information storage capacity: $Q_{mem} \to N$.

#### 3. Derivation of Scalar Perturbations and Curvature Mapping

In standard inflationary cosmology, the primordial curvature perturbation $\zeta$ is generated by the quantum fluctuations of a scalar field (the inflaton). In the memory burden framework, inflation is driven by the graviton condensate itself, and the perturbations must be mapped directly from the fluctuations of the condensate and its memory burden.

The gauge-invariant curvature perturbation $\zeta$ on super-horizon scales is related to the fractional fluctuation in the local expansion history, which in this model corresponds to the fractional fluctuation in the condensate occupation number:
<code>
\zeta \sim \frac{\delta N}{N}
</code>
Since $N = M_{Pl}^2 / H^2$, fluctuations in $N$ are directly tied to fluctuations in the local Hubble parameter. The memory burden acts as a self-regulating pressure $p_{mem}$ that stabilizes the condensate. The effective speed of sound for these fluctuations is given by:
<code>
c_s^2 = \frac{\partial p_{mem}}{\partial \rho_{cond}}
</code>
For the gapless Bogoliubov modes at the quantum critical point, the dispersion relation $\epsilon_k \sim k$ (for $\delta = 1$) implies that the excitations propagate at the speed of light, yielding $c_s \approx 1$. This ensures that the perturbations do not exhibit the strong non-Gaussianities typically associated with low speed of sound models ($f_{NL} \propto 1/c_s^2$).

The power spectrum of the curvature perturbations is determined by the energy scale of the condensate and the slow-roll-equivalent parameters. In the corpuscular model, the amplitude of the scalar power spectrum is:
<code>
\Delta_\zeta^2 \sim \frac{1}{N} \sim \frac{H^2}{M_{Pl}^2}
</code>
which naturally matches the observed amplitude $A_s \sim 10^{-9}$ for $H/M_{Pl} \sim 10^{-5} - 10^{-4}$.

The spectral index $n_s$ measures the scale dependence of the power spectrum:
<code>
n_s - 1 = \frac{d \ln \Delta_\zeta^2}{d \ln k}
</code>
During the metastable quasi-de Sitter phase, the feedback mechanism ensures $dN/dt \approx 0$, meaning $H$ is approximately constant. However, the slow accumulation of memory $Q_{mem}$ introduces a slight time dependence to the effective Hubble parameter. The effective slow-roll parameter $\epsilon = -\dot{H}/H^2$ is related to the depletion rate:
<code>
\epsilon \sim \frac{1}{H N} \left| \frac{dN}{dt} \right|
</code>
Because the memory burden stabilizes the condensate, $\epsilon$ is extremely small but non-zero as the system slowly drifts toward the quantum breaking point. The spectral index is given by $n_s - 1 \approx -2\epsilon - \eta$, where $\eta$ is related to the second derivative of the condensate evolution. The slight red tilt observed in the CMB ($n_s \approx 0.96$) is thus a direct consequence of the finite lifetime of the condensate and the gradual increase in the memory load, which slowly decreases the effective energy scale of the horizon before quantum breaking occurs.

This mapping demonstrates that the memory burden mechanism not only provides a dynamical origin for the de Sitter background but also naturally sources the nearly scale-invariant, Gaussian curvature perturbations required by observational cosmology, replacing the ad-hoc inflaton potential with the fundamental information-theoretic dynamics of quantum gravity.