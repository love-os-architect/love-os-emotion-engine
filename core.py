import numpy as np

class LoveOS_Physics:
    """
    The Core Physics Engine of Love-OS.
    Simulates internal state dynamics using Euler method.
    """
    def __init__(self):
        """
        State vector z = [R, L, E, C]
          R: Unexplained info / prediction error accumulation
          L: Love / integration capacity
          E: Ego / defensiveness (separation bias)
          C: Sense of control / agency
        """
        # Slightly positive stable initial state
        self.z = np.array([0.1, 0.5, 0.2, 0.5], dtype=float)

        # Physics-informed coefficients (Love-OS v0.95)
        self.params = {
            'aR': 1.2, 'bR': 0.8, 'gR': 0.6,   # dR = +aR*Δ - bR*L*R - gR*C*R
            'aL': 0.4, 'bL': 0.3, 'dL': 0.05,  # dL = +aL*C - bL*E*R - dL*L + uL
            'aE': 0.8, 'bE': 0.5, 'dE': 0.1,   # dE = +aE*|Δ| - bE*L - dE*E + uE
            'aC': 0.5, 'bC': 0.6, 'dC': 0.1    # dC = -aC*R + bC*L - dC*C + uC
        }

        # Physical time (seconds) advanced per conversation turn
        self.dt = 0.5
        # Integration depth per turn (more steps -> richer "afterglow")
        self.steps_per_turn = 5

    def step(self, delta_val: float, ritual_type: str | None = None):
        """
        Update the physical state by one conversation turn.
        delta_val : external stimulus / prediction error Δ
        ritual_type : 'BREATH', 'LABEL', or None
        """
        # Ritual inputs (uL, uC, uE) and Δ attenuation
        uL, uC, uE = 0.0, 0.0, 0.0
        eff_delta = float(delta_val)

        if ritual_type == 'BREATH':
            # Deep breathing: reduce Ego, restore Control, dampen Δ
            uE = -0.3
            uC = +0.2
            eff_delta *= 0.6
        elif ritual_type == 'LABEL':
            # Affective labeling: induce integration (Love)
            uL = +0.3
            eff_delta *= 0.8

        # Euler integration for several micro-steps
        for _ in range(self.steps_per_turn):
            R, L, E, C = self.z
            p = self.params

            dR = p['aR'] * eff_delta - p['bR'] * L * R - p['gR'] * C * R
            dL = p['aL'] * C - p['bL'] * E * R - p['dL'] * L + uL
            dE = p['aE'] * abs(eff_delta) - p['bE'] * L - p['dE'] * E + uE
            dC = -p['aC'] * R + p['bC'] * L - p['dC'] * C + uC

            # Update & clip (anti-explosion safety)
            self.z += np.array([dR, dL, dE, dC]) * (self.dt / self.steps_per_turn)
            self.z = np.clip(self.z, -2.0, 2.0)

        return self.z

    def get_observation(self):
        """
        Map state to observable affect:
          Valence: pleasant(+) / unpleasant(-)
          Arousal: activation
        """
        R, L, E, C = self.z
        valence = np.tanh(1.0 * (-R) + 0.8 * L - 1.0 * E + 0.7 * C)
        # Using softplus-ish form with R,E as proxies of activation
        arousal = np.log1p(np.exp(0.5 * abs(R) + 0.5 * E))
        return valence, arousal
