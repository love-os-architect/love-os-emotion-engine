```python
# -*- coding: utf-8 -*-
"""
Love-OS Dynamics Engine
Core Physics: S = Integral |I - A| dt

This module simulates the dynamic relationship between:
- I(t): Impulse (Internal Signal)
- A(t): Action (External Output)
- S:    Shame (Hysteresis Loss)
"""

from collections import deque
from dataclasses import dataclass
from typing import Callable, Tuple, List, Optional
import math

Array = List[float]

# -----------------------------
# Stimulus Functions (F(t))
# -----------------------------
def pulse_train(amp: float = 1.0, width: float = 0.2, period: float = 2.0) -> Callable[[float], float]:
    """Square wave pulse train."""
    def F(t: float) -> float:
        tt = (t % period)
        return amp if tt < width else 0.0
    return F

def sine_stim(amp: float = 1.0, freq: float = 0.5) -> Callable[[float], float]:
    """Sinusoidal stimulus."""
    def F(t: float) -> float:
        return amp * math.sin(2 * math.pi * freq * t)
    return F

def impulse(at: float = 1.0, amp: float = 1.0, eps: float = 1e-3) -> Callable[[float], float]:
    """Single impulse (Dirac delta approximation)."""
    def F(t: float) -> float:
        return amp if abs(t - at) < eps else 0.0
    return F

# -----------------------------
# The Shame Model
# -----------------------------
@dataclass
class ShameModel:
    """
    Love-OS Dynamical Model
    tau   : Latency/Lag (Censorship time)
    alpha : Damping coefficient (Suppression of Impulse)
    r_int : Internal Resistance (Self-Conflict)
    """
    tau: float = 0.3       
    alpha: float = 0.2     
    r_int: float = 0.05    
    sc_eps: float = 1e-3   # Threshold for Superconductivity

    def is_superconductive(self) -> bool:
        """Check if the system is in a superconducting state (Zero Resistance/Latency)."""
        return (self.tau <= self.sc_eps) and \
               (self.alpha <= self.sc_eps) and \
               (self.r_int <= self.sc_eps)

    def simulate(
        self,
        T: float = 10.0,
        dt: float = 0.001,
        stimulus: Optional[Callable[[float], float]] = None,
        use_delay: bool = True
    ) -> Tuple[Array, Array, Array, Array, float]:
        """
        Run the simulation.
        Returns: time, I, A, s(instant), S(total)
        """
        if stimulus is None:
            stimulus = pulse_train()

        n = int(T / dt)
        time: Array = [0.0] * (n + 1)
        I: Array = [0.0] * (n + 1)
        A: Array = [0.0] * (n + 1)
        s: Array = [0.0] * (n + 1) # Instantaneous shame

        # Delay Buffer
        delay_steps = max(1, int(self.tau / dt)) if use_delay else 1
        I_history = deque([0.0] * delay_steps, maxlen=delay_steps)

        # Initial Conditions
        t, i, a, S_acc = 0.0, 0.0, 0.0, 0.0

        for k in range(n + 1):
            time[k] = t
            I[k] = i
            A[k] = a
            
            # Calculate Instantaneous Shame (Physics: Deviation)
            s[k] = abs(i - a)
            S_acc += s[k] * dt

            # Apply Stimulus
            F = stimulus(t)

            # --- Impulse Dynamics (Inner World) ---
            # dI/dt = Input - Damping - Internal_Conflict
            sign = 0.0 if (abs(i - a) < 1e-12) else ((i - a) / abs(i - a))
            di = F - self.alpha * i - self.r_int * sign * abs(i - a)
            i_next = i + dt * di

            # --- Action Dynamics (Outer World) ---
            # dA/dt tracks I (with delay)
            if self.tau <= 0.0 or not use_delay:
                # Zero Latency Mode
                tau_eff = max(self.tau, dt) if self.tau > 0.0 else dt
                da = (i - a) / tau_eff
                a_next = a + dt * da
            else:
                # Delayed Mode
                i_delay = I_history[0]  # Fetch I(t - tau)
                da = (i_delay - a) / self.tau
                a_next = a + dt * da

            # Update Buffer
            if use_delay and self.tau > 0.0:
                I_history.append(i_next)

            # Step Forward
            i, a = i_next, a_next
            t += dt

        return time, I, A, s, S_acc

    @staticmethod
    def coherence(I: Array, A: Array) -> float:
        """
        Calculate Phase Coherence (-1.0 to 1.0).
        1.0 means Action perfectly mirrors Impulse (Superconductivity).
        """
        n = len(I)
        if n != len(A) or n == 0: return 0.0
        meanI = sum(I) / n
        meanA = sum(A) / n
        num = sum((i - meanI) * (a - meanA) for i, a in zip(I, A))
        denI = math.sqrt(sum((i - meanI) ** 2 for i in I)) + 1e-12
        denA = math.sqrt(sum((a - meanA) ** 2 for a in A)) + 1e-12
        return num / (denI * denA)

if __name__ == "__main__":
    # Quick Test
    model = ShameModel(tau=0.4, alpha=0.25, r_int=0.05)
    T, I, A, s, S = model.simulate(T=6.0, dt=0.001, stimulus=pulse_train())
    print(f"Total Shame (S) = {S:.6f}, Coherence = {model.coherence(I, A):.3f}")
ファイル名: loveos_dsl.py (Layer 2: DSL Parser)

Python
# -*- coding: utf-8 -*-
"""
Love-OS Dynamics DSL Parser
Enables defining internal states via simple commands.
"""

from typing import List, Tuple, Dict, Any
import re
from loveos_dynamics import ShameModel, pulse_train, sine_stim, impulse

DEFAULTS = dict(
    tau=0.3, alpha=0.2, r_int=0.05, T=6.0, dt=0.001, use_delay=True,
    stim=('PULSE', (1.0, 0.2, 2.0))
)

def parse_and_run(lines: List[str]) -> Dict[str, Any]:
    cfg = DEFAULTS.copy()
    
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            continue

        toks = re.split(r'\s+', line)
        cmd = toks[0].upper()

        # Command Parsing
        if cmd == 'SC' and toks[1].upper() == 'ON':
            # Enter Superconductivity State
            cfg['tau'] = 0.0
            cfg['alpha'] = 1e-6
            cfg['r_int'] = 1e-6
            cfg['use_delay'] = False
        elif cmd == 'SC' and toks[1].upper() == 'OFF':
            # Return to Normal State
            cfg['tau'] = DEFAULTS['tau']
            cfg['alpha'] = DEFAULTS['alpha']
            cfg['r_int'] = DEFAULTS['r_int']
            cfg['use_delay'] = True
        elif cmd == 'TAU':
            cfg['tau'] = float(toks[1])
        elif cmd == 'ALPHA':
            cfg['alpha'] = float(toks[1])
        elif cmd == 'RINT':
            cfg['r_int'] = float(toks[1])
        elif cmd == 'T':
            cfg['T'] = float(toks[1])
        elif cmd == 'DT':
            cfg['dt'] = float(toks[1])
        elif cmd == 'DELAY':
            cfg['use_delay'] = toks[1].lower() == 'on'
        
        # Stimulus Configuration
        elif cmd == 'PULSE':
            cfg['stim'] = ('PULSE', tuple(map(float, toks[1:4])))
        elif cmd == 'SINE':
            cfg['stim'] = ('SINE', tuple(map(float, toks[1:3])))
        elif cmd == 'IMPULSE':
            cfg['stim'] = ('IMPULSE', tuple(map(float, toks[1:3])))
        else:
            raise ValueError(f"Unknown Command: {line}")

    # Build Stimulus
    stim_kind, params = cfg['stim']
    if stim_kind == 'PULSE':   stim = pulse_train(*params)
    elif stim_kind == 'SINE':  stim = sine_stim(*params)
    elif stim_kind == 'IMPULSE': stim = impulse(*params)
    else: raise ValueError(f"Unknown Stimulus: {stim_kind}")

    # Execute Simulation
    model = ShameModel(tau=cfg['tau'], alpha=cfg['alpha'], r_int=cfg['r_int'])
    T, I, A, s, S = model.simulate(T=cfg['T'], dt=cfg['dt'], stimulus=stim, use_delay=cfg['use_delay'])
    
    return {
        "S": S,
        "coherence": ShameModel.coherence(I, A),
        "is_sc": model.is_superconductive(),
        "data": {"T": T, "I": I, "A": A, "s": s}
    }
