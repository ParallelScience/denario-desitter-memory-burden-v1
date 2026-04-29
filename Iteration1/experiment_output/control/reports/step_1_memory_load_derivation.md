<!-- filename: reports/step_1_memory_load_derivation.md -->
# Microscopic Derivation of the Memory Load Functional $F(M_{Pl}/H)$

## 1. Density of States and Occupation of Bogoliubov Modes
In the corpuscular framework, a Hubble patch of de Sitter spacetime is described as a critical condensate of $N = M_{Pl}^2/H^2$ soft gravitons. Small fluctuations around this background manifest as collective Bogoliubov excitations, which serve as the primary channels for information storage. The total memory load $Q_{mem}$ is defined as the integrated occupation number of these near-gapless modes within a Hubble volume $V \sim H^{-3}$:

<code>Q_{mem} = \sum_k \langle b_k^\dagger b_k \rangle \approx V \int \frac{d^3k}{(2\pi)^3} \langle n_k \rangle</code>

The modes are populated thermally according to the Bose-Einstein distribution at the Gibbons-Hawking temperature $T = H / 2\pi$. Because the Bogoliubov modes are near-gapless, their energy $\epsilon_k$ is much smaller than the temperature ($\epsilon_k \ll T$). This allows us to approximate the occupation number using the Rayleigh-Jeans tail:

<code>\langle n_k \rangle \approx \frac{T}{\epsilon_k} \sim \frac{H}{\epsilon_k}</code>

To capture the collective nature of these excitations, we parameterize their dispersion relation as a generic power law:

<code>\epsilon_k = H \left( \frac{k}{H} \right)^\delta</code>

where the exponent $\delta \ge 1$ characterizes the softness of the modes. Standard relativistic modes correspond to $\delta = 1$, while $\delta > 1$ represents sub-extensive, highly soft collective excitations of the condensate.

## 2. Phase Space Integration and Holographic Constraints
Substituting the occupation number and dispersion relation into the phase space integral, the memory load per species, denoted as $F(x)$ where $x = M_{Pl}/H$, is given by:

<code>F(x) \sim H^{-3} \int_{k_{min}}^{H} k^2 dk \frac{H}{H (k/H)^\delta} \sim \int_{y_{min}}^{1} y^{2-\delta} dy</code>

where $y = k/H$ is the dimensionless momentum. The ultraviolet (UV) cutoff is naturally set by the horizon scale $k_{max} \sim H$ (so $y_{max} = 1$). The infrared (IR) cutoff $k_{min}$ is determined by the mass gap of the condensate. The lowest possible energy of a Bogoliubov mode in a condensate of $N$ constituents is $\epsilon_{min} \sim 1/N \sim H^2/M_{Pl}^2$. Equating this mass gap to the dispersion relation yields the IR momentum cutoff:

<code>H y_{min}^\delta \sim \frac{H^2}{M_{Pl}^2} \implies y_{min} \sim \left( \frac{H}{M_{Pl}} \right)^{1/\delta} = x^{-1/\delta}</code>

The scaling of the integral $\int_{y_{min}}^1 y^{2-\delta} dy$ depends critically on the exponent $\delta$. The total number of accessible modes is fundamentally bounded by the holographic entropy constraint $S_{dS} \sim M_{Pl}^2/H^2$, ensuring that the phase space volume does not over-count degrees of freedom beyond the Bekenstein-Hawking limit.

## 3. Tabulation of Functional Forms for $F(x)$
Evaluating the phase space integral for different regimes of $\delta$ yields distinct functional forms for $F(x)$. These forms dictate how the memory burden scales with the de Sitter curvature and form the basis for the dynamical selection equation $N_s F(M_{Pl}/H) \sim M_{Pl}^2/H^2$. We explicitly tabulate these forms below to provide a precise, unambiguous set of models for subsequent numerical implementation.

| Model | Functional Form $F(x)$ | Dispersion Exponent | Physical Justification |
| :--- | :--- | :--- | :--- |
| **Constant** | $F(x) = 1$ | $\delta < 3$ | The integral is UV-dominated. Information is primarily stored in horizon-scale fluctuations (e.g., standard relativistic modes with $\delta=1$). The memory capacity per species is independent of the condensate size $N$, representing localized, weakly-coupled information storage. |
| **Logarithmic** | $F(x) = \ln(x)$ | $\delta = 3$ | The integral yields a logarithmic dependence on the IR cutoff. This represents a scale-invariant distribution of information, where each logarithmic momentum shell contributes equally to the memory burden. This is characteristic of holographic systems where information is uniformly spread across all available scales. |
| **Power-Law ($\alpha=0.5$)** | $F(x) = x^{0.5}$ | $\delta = 6$ | The integral is IR-dominated, scaling as $x^\alpha$ with $\alpha = 1 - 3/\delta$. Information storage is concentrated in the deepest IR modes (collective condensate excitations). The memory capacity grows as the square root of the condensate size, indicating strong entanglement. |
| **Power-Law ($\alpha=1.0$)** | $F(x) = x^{1.0}$ | $\delta \to \infty$ | Represents an extreme limit of soft modes where the memory load scales linearly with $x = M_{Pl}/H$. This implies the memory burden per species is proportional to the square root of the de Sitter entropy. |
| **Power-Law ($\alpha=2.0$)** | $F(x) = x^{2.0}$ | Phenomenological | A phenomenological upper bound where $F(x) \sim N$. In this regime, a single species is sufficient to saturate the memory burden, dynamically enforcing $N_s \sim 1$ and saturating the species bound. |

*(Note for numerical implementation: The pre-factors for all functional forms have been set to unity to isolate the scaling behavior and facilitate direct evaluation of the dynamical selection mechanism.)*

This derivation establishes a rigorous, first-principles basis for the memory load functional, directly linking the microscopic density of states of the graviton condensate to the macroscopic dynamical selection of the inflationary Hubble scale.