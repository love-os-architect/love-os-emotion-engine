# Love-OS: Interactive Phase Transition Simulator

**Version:** 1.0 (GUI Edition)
**Core Architecture:** Hopf Normal Form (Virtual/Phase) + Landau Free Energy (Reality)

This interactive Jupyter Notebook simulates the non-linear dynamics of "Reality Creation" and "Phase Locking." It visually demonstrates how accumulating internal energy ($R$), resisting environmental drift ($\omega$), and injecting intentional pulses ($\Delta v$) lead to the spontaneous emergence of a new reality ($X$).

## The Mathematical Model

1.  **The Virtual Axis (Complex Amplitude & Phase):**
    $$\dot{R} = \mu R - \beta R^3$$
    $$\dot{\theta} = \omega - \gamma R^2 - K_0 R \sin(\theta - \theta_0) + \sigma \eta(t)$$
    * $R$: Internal accumulation (Love, Introspection, Mastery).
    * $\theta$: Phase angle (Trajectory/Intent).
    * $\omega$: Environmental drift (Societal gravity pulling you down).
    * $\sigma$: Unpredictable noise (Daily friction/chaos).
    * $K_0 R$: Synchronization strength. When this overpowers $\omega$, phase lock occurs.

2.  **The Real Axis (Landau Reality Order):**
    $$\mathcal{F}(X; R) = \frac{\alpha(R_c - R)}{2}X^2 + \frac{b}{4}X^4$$
    $$\dot{X} = -\frac{\partial \mathcal{F}}{\partial X} - c \sin(\theta - \theta_0)$$
    * $X$: Visible reality. Remains $0$ until $R$ crosses the critical threshold $R_c$.

3.  **The Pulse ($\Delta v$):** A manual override representing a bold decision, a boundary set, or a profound realization. It forces an immediate phase shift ($\theta \leftarrow \theta + \phi$), snapping the trajectory back toward the True North Star ($\theta_0$).

## Usage Instructions
Run the provided notebook cell in a Jupyter environment. Use the interactive sliders to adjust gravity, noise, and love gain. Click the **[Inject $\Delta v$]** button to simulate a conscious trajectory correction and watch the system stabilize and manifest reality.
