<!-- filename: reports/step_1_memory_load_derivation.md -->
# Derivation of the Memory Load Functional $F(M_{Pl}/H)$

The memory load $Q_{mem}$ is defined as the total number of excited Bogoliubov modes $b_k$ within the graviton condensate. The condensate is confined to a Hubble patch of volume $V \sim H^{-3}$. The density of states in momentum space is given by $d^3k / (2\pi)^3$. For $N_s$ particle species, the total memory load is obtained by integrating the occupation number $n_k = \langle b_k^\dagger b_k \rangle$ over the available phase space, from the infrared cutoff (the Hubble scale $H$) to the ultraviolet cutoff (the Planck scale $M_{Pl}$):

<code>Q_{mem} \approx N_s V \int_{H}^{M_{Pl}} \frac{d^3k}{(2\pi)^3} n_k \sim N_s H^{-3} \int_{H}^{M_{Pl}} k^2 n_k dk</code>

The functional form of $F(M_{Pl}/H)$ is entirely determined by the spectrum of the occupation number $n_k$. In a de Sitter background, the occupation number of light or gapless modes typically follows a power-law spectrum $n_k \sim (H/k)^\alpha$, where the exponent $\alpha$ depends on the specific coupling and spin of the modes.

Substituting this spectrum into the phase space integral yields:

<code>Q_{mem} \sim N_s H^{\alpha-3} \int_{H}^{M_{Pl}} k^{2-\alpha} dk</code>

We can now evaluate this integral for different values of $\alpha$ to justify the various functional forms of $F(M_{Pl}/H) = Q_{mem}/N_s$:

*   **Linear scaling ($F \sim M_{Pl}/H$):** If the occupation number scales as $n_k \sim (H/k)^2$ (e.g., for conformally coupled fields or specific Bogoliubov excitations), the integral becomes $\int_{H}^{M_{Pl}} dk \approx M_{Pl}$ (assuming $M_{Pl} \gg H$). This gives $Q_{mem} \sim N_s H^{-1} M_{Pl} = N_s (M_{Pl}/H)$. Thus, $F(M_{Pl}/H) \sim M_{Pl}/H$. This serves as our primary functional form.
*   **Logarithmic scaling ($F \sim \log(M_{Pl}/H)$):** If the spectrum is scale-invariant, $n_k \sim (H/k)^3$, the integral is $\int_{H}^{M_{Pl}} k^{-1} dk = \log(M_{Pl}/H)$. This yields $Q_{mem} \sim N_s \log(M_{Pl}/H)$, corresponding to $F(M_{Pl}/H) \sim \log(M_{Pl}/H)$.
*   **Constant scaling ($F = \text{const}$):** If the spectrum is highly red-tilted, e.g., $n_k \sim (H/k)^4$, the integral is dominated by the infrared cutoff: $\int_{H}^{M_{Pl}} k^{-2} dk \approx H^{-1}$. This gives $Q_{mem} \sim N_s H \cdot H^{-1} = N_s$, corresponding to $F(M_{Pl}/H) \sim \text{const}$.
*   **General power-law scaling ($F \sim (M_{Pl}/H)^p$):** For a generic exponent $\alpha = 3 - p$ (with $p > 0$), the integral is dominated by the UV cutoff, yielding $Q_{mem} \sim N_s (M_{Pl}/H)^p$.

# Dynamical Selection Equation and Preferred Hubble Scale

The dynamical selection mechanism posits that the quasi-de Sitter phase is stabilized when the memory load saturates the condensate capacity, $Q_{mem} \sim N$. Given $N = M_{Pl}^2/H^2$, the stabilization condition becomes:

<code>N_s F\left(\frac{M_{Pl}}{H}\right) \sim \frac{M_{Pl}^2}{H^2}</code>

We now analyze whether this equation yields a unique preferred Hubble scale $H$ for the three specific functional forms. Let $x = M_{Pl}/H \gg 1$. The selection equation is $N_s F(x) \sim x^2$.

## Case 1: Constant Form ($F = C$)
If $F(x) = C$, the selection equation is:
<code>N_s C \sim x^2 \implies \frac{M_{Pl}^2}{H^2} \sim C N_s</code>
Solving for $H$, we find:
<code>H \sim \frac{M_{Pl}}{\sqrt{C N_s}}</code>
**Conclusion:** This form yields a **unique preferred $H$** that is inversely proportional to the square root of the number of species.

## Case 2: Logarithmic Form ($F \sim \log(M_{Pl}/H)$)
If $F(x) = \beta \log x$, the selection equation is:
<code>N_s \beta \log x \sim x^2 \implies \frac{x^2}{\log x} \sim \beta N_s</code>
For $x > \sqrt{e}$ (which is guaranteed since $M_{Pl}/H \gg 1$), the function $f(x) = x^2/\log x$ is strictly monotonically increasing. Therefore, for any given $N_s \ge 1$, there is exactly one solution for $x$.
**Conclusion:** This form yields a **unique preferred $H$**. The solution can be expressed analytically in terms of the Lambert W function, $H \sim M_{Pl} / \sqrt{-\frac{1}{2} W_{-1}(-\frac{2}{\beta N_s})}$, which asymptotically scales as $H \sim M_{Pl} / \sqrt{N_s \log N_s}$.

## Case 3: Power-Law Form ($F \sim (M_{Pl}/H)^p$)
If $F(x) = \lambda x^p$, the selection equation is:
<code>N_s \lambda x^p \sim x^2 \implies x^{2-p} \sim \lambda N_s</code>
The existence of a unique $H$ depends critically on the exponent $p$:
*   **If $p < 2$:** The equation gives $x \sim (\lambda N_s)^{1/(2-p)}$, which yields a **unique preferred $H \sim M_{Pl} / (\lambda N_s)^{1/(2-p)}$**. For our primary linear scaling ($p=1$), this gives $H \sim M_{Pl} / (\lambda N_s)$.
*   **If $p = 2$:** The equation reduces to $N_s \lambda \sim 1$. The dependence on $x$ (and thus $H$) completely cancels out. This does **not** yield a preferred $H$; instead, it only provides an inequality/constraint on the number of species (requiring $N_s \sim 1/\lambda$). In this scenario, $H$ is dynamically unconstrained by the memory burden saturation.
*   **If $p > 2$:** The equation gives $x^{p-2} \sim 1/(\lambda N_s)$. Since $x = M_{Pl}/H \gg 1$, this would require $N_s \ll 1$, which violates the physical requirement $N_s \ge 1$. Thus, no valid de Sitter solution exists for $p > 2$.

**Conclusion:** The power-law form yields a **unique preferred $H$ only if $p < 2$**. If $p = 2$, it yields only a constraint on $N_s$ and leaves $H$ undetermined.