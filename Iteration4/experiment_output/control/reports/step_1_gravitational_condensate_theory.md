<!-- filename: reports/step_1_gravitational_condensate_theory.md -->
# Background Theoretical Derivations

The corpuscular theory of gravity posits that a Hubble patch of de Sitter spacetime is not a fundamental vacuum, but rather a coherent bound state—a condensate—of $N$ soft gravitons. The occupation number of this condensate is given by $N = M_{Pl}^2 / H^2$, where $H$ is the Hubble parameter. In this framework, the de Sitter entropy is equivalent to the number of constituents, $S_{dS} \sim N$. The collective coupling of the gravitons is $\alpha \sim 1/N$, placing the system at a point of quantum criticality ($\alpha N \sim 1$). 

Below, we formalize the theoretical derivations that govern the stability, the species constraints, and the maximum duration of the inflationary epoch within this paradigm.

## 1. Dynamical Generation of de Sitter and the Metastable Fixed Point

Small fluctuations around the graviton condensate manifest as Bogoliubov modes with near-gapless energy $\epsilon_k \sim 1/N$. These modes serve as information storage channels, and their excitation leads to a "memory burden" $Q_{mem}$ that backreacts on the condensate. 

The time evolution of the graviton occupation number $N$ is governed by the competition between the natural depletion of the condensate and the stabilizing backreaction from the memory burden. This is described by the feedback equation:
<code>\frac{dN}{dt} = -H + \gamma \frac{Q_{mem}}{N^2}</code>
where $\gamma$ is a dimensionless coupling constant. 

Working in Planck units ($M_{Pl} = 1$), the relation between the occupation number and the Hubble parameter simplifies to $H = N^{-1/2}$. Substituting this into the evolution equation yields:
<code>\frac{dN}{dt} = -N^{-1/2} + \gamma \frac{Q_{mem}}{N^2}</code>

A metastable quasi-de Sitter state—characteristic of the inflationary epoch—emerges when the depletion is exactly counteracted by the memory burden, leading to a constant Hubble parameter. We find this fixed point by setting $dN/dt = 0$:
<code>0 = -N^{-1/2} + \gamma \frac{Q_{mem}^*}{N^2}</code>

Solving for the critical memory load $Q_{mem}^*$, we obtain:
<code>Q_{mem}^* = \frac{N^2 \cdot N^{-1/2}}{\gamma} = \frac{N^{3/2}}{\gamma}</code>

This derivation demonstrates that a quasi-de Sitter phase can be dynamically stabilized without the need for a fundamental, bare cosmological constant. The memory burden itself provides the necessary feedback mechanism to maintain $H \approx \text{const}$.

## 2. The Species Bound from the Gravitational Cutoff

In a universe populated by $N_s$ distinct particle species, the fundamental scale of gravity is lowered from the Planck mass to the species scale (or gravitational cutoff), defined as:
<code>\Lambda_g \simeq \frac{M_{Pl}}{\sqrt{N_s}}</code>

For the semiclassical description of the de Sitter spacetime to remain theoretically consistent, the characteristic energy scale of the spacetime—given by the Hubble parameter $H$—must not exceed this gravitational cutoff. Imposing the consistency condition $H \leq \Lambda_g$ yields:
<code>H \leq \frac{M_{Pl}}{\sqrt{N_s}}</code>

Squaring both sides and rearranging for the number of species $N_s$, we find:
<code>N_s \leq \frac{M_{Pl}^2}{H^2}</code>

Recognizing that the de Sitter entropy is given by $S_{dS} \sim N = M_{Pl}^2 / H^2$, this inequality establishes a fundamental bound: the number of particle species cannot exceed the de Sitter entropy, $N_s \leq S_{dS}$.

## 3. Quantum Breaking and the $N_e$-$N_s$ Relation

The memory load accumulates over time due to the continuous production of Bogoliubov modes. The rate of this accumulation is proportional to the number of available particle species $N_s$ and the Hubble rate $H$:
<code>\frac{dQ_{mem}}{dt} \simeq N_s H</code>

Assuming the memory load starts at $Q_{mem}(0) = 0$, the time required to reach the saturation point $Q_{mem} \sim N$ defines the quantum breaking time $t_{qb}$. At this point, the memory burden overcomes the condensate stability, and semiclassicality breaks down. Integrating the accumulation rate gives:
<code>Q_{mem}(t_{qb}) \simeq N_s H t_{qb} \sim N</code>

Solving for $t_{qb}$ and substituting $N = M_{Pl}^2 / H^2$, we obtain the quantum breaking time:
<code>t_{qb} \simeq \frac{N}{N_s H} = \frac{M_{Pl}^2}{N_s H^3}</code>

The duration of the inflationary quasi-de Sitter phase, $t_{life}$, is directly related to the number of e-folds $N_e$ by the relation $N_e = H t_{life}$. For inflation to successfully proceed for $N_e$ e-folds before the onset of quantum breaking, the lifetime of the condensate must be strictly bounded by the quantum breaking time, $t_{life} \leq t_{qb}$. Substituting the expressions for $t_{life}$ and $t_{qb}$ yields:
<code>\frac{N_e}{H} \leq \frac{M_{Pl}^2}{N_s H^3}</code>

Multiplying both sides by $H$, we arrive at the central inequality linking the inflationary duration, the species count, and the Hubble scale:
<code>N_e \leq \frac{M_{Pl}^2}{N_s H^2}</code>

Alternatively, this can be expressed as $N_e \cdot N_s \leq M_{Pl}^2 / H^2$. This key relation demonstrates a strict dynamical trade-off: a larger number of particle species accelerates the accumulation of the memory burden, thereby shortening the maximum possible duration of the inflationary epoch before quantum breaking occurs.