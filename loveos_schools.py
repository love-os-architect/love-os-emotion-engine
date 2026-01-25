import math
import csv
import copy
import random
import matplotlib.pyplot as plt
from dataclasses import dataclass, field, replace

# ==========================================
# 0) Core Physics (Love-OS ODE Kernel)
# ==========================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

@dataclass
class Params:
    # Standard Love-OS v0.95 parameters (The "Average" Human)
    aR: float = 1.2; bR: float = 0.8; gR: float = 0.6
    aL: float = 0.4; bL: float = 0.3; dL: float = 0.05
    aE: float = 0.8; bE: float = 0.5; dE: float = 0.1
    aC: float = 0.5; bC: float = 0.6; dC: float = 0.1

@dataclass
class RLEC:
    """The State Vector of the Heart"""
    R: float = 0.1 # Resistance (Confusion/Error)
    L: float = 0.5 # Love (Integration)
    E: float = 0.2 # Ego (Separation/Defense)
    C: float = 0.5 # Control (Agency)
    dt: float = 0.5
    steps: int = 5
    p: Params = field(default_factory=Params)

    def step(self, delta, uL=0.0, uC=0.0, uE=0.0):
        # Euler Integration (Neural ODE approximation)
        for _ in range(self.steps):
            R, L, E, C = self.R, self.L, self.E, self.C
            p = self.p
            
            # The Unified Equation of Emotion
            dR = p.aR*delta - p.bR*L*R - p.gR*C*R
            dL = p.aL*C - p.bL*E*R - p.dL*L + uL
            dE = p.aE*abs(delta) - p.bE*L - p.dE*E + uE
            dC = -p.aC*R + p.bC*L - p.dC*C + uC

            self.R = clamp(self.R + (self.dt/self.steps)*dR, -2.0, 3.0)
            self.L = clamp(self.L + (self.dt/self.steps)*dL, -2.0, 3.0)
            self.E = clamp(self.E + (self.dt/self.steps)*dE, -2.0, 3.0)
            self.C = clamp(self.C + (self.dt/self.steps)*dC, -2.0, 3.0)

    def observe(self):
        """Map internal state to Valence/Arousal"""
        val = math.tanh(1.0*(-self.R) + 0.8*self.L - 1.0*self.E + 0.7*self.C)
        aro = math.log1p(math.exp(0.5*abs(self.R) + 0.5*self.E))
        return val, aro

# ==========================================
# 1) School Specifications (The Unified Ontology)
# ==========================================

# Ritual Dictionary (Unified Right-Brain DSL)
RITUALS = {
    'BREATH':     {'uL':0.0,  'uC':+0.2,  'uE':-0.3,  'd_scale':0.6},
    'LABEL':      {'uL':+0.3, 'uC':0.0,   'uE':0.0,   'd_scale':0.8},
    'REAPPRAISE': {'uL':+0.25,'uC':+0.15, 'uE':-0.15, 'd_scale':0.7}, # CBT
    'ACT':        {'uL':+0.2, 'uC':+0.2,  'uE':-0.1,  'd_scale':0.8}, # ACT
    'INTERPRET':  {'uL':+0.3, 'uC':0.0,   'uE':-0.1,  'd_scale':0.9}, # Psychodynamic
    'RELATEDNESS':{'uL':+0.3, 'uC':+0.1,  'uE':-0.2,  'd_scale':0.7}, # Attachment
    'COMPASSION': {'uL':+0.4, 'uC':0.0,   'uE':-0.3,  'd_scale':0.6}, # Mindfulness
    'EXPOSURE':   {'uL':0.0,  'uC':+0.3,  'uE':+0.1,  'd_scale':0.9}, # Behavioral
    'AUTONOMY':   {'uL':0.1,  'uC':+0.4,  'uE':0.0,   'd_scale':0.9}, # SDT
    'NONE':       {'uL':0.0,  'uC':0.0,   'uE':0.0,   'd_scale':1.0},
}

def delta_basic(V, A): 
    # Basic mapping from Valence/Arousal to Prediction Error (Delta)
    return clamp(0.8*A - 0.6*V, -1.5, 1.5)

def shift_params(base: Params, **kwargs):
    new_p = replace(base)
    for k, v in kwargs.items():
        if hasattr(new_p, k):
            setattr(new_p, k, getattr(new_p, k) + v)
    return new_p

class SchoolSpec:
    def __init__(self, name, param_shifter, delta_func, policy_func):
        self.name = name
        self.param_shifter = param_shifter
        self.delta_func = delta_func
        self.policy_func = policy_func

# --- The 8 Schools of Psychology implemented as Math ---

# 1. CBT (Cognitive Behavioral Therapy)
# Focus: Reappraisal. High cognitive control.
def cbt_p(p): return shift_params(p, bR=+0.1, aL=+0.1, bC=+0.1, dE=+0.05, aE=-0.1)
def cbt_d(V,A): return 0.95 * delta_basic(V,A)
def cbt_pol(z,V,A): return 'REAPPRAISE' if z.R > 0.7 else 'NONE'

# 2. ACT (Acceptance & Commitment Therapy)
# Focus: Psychological Flexibility. Accepting Ego/R, moving with Values (C).
def act_p(p): return shift_params(p, aL=+0.1, aC=+0.1, aE=-0.1)
def act_d(V,A): return 0.90 * delta_basic(V,A)
def act_pol(z,V,A): return 'ACT' if z.E > 0.8 else 'NONE'

# 3. Psychodynamic (Psychoanalysis)
# Focus: Insight. Slow dynamics. Resolving R and E deep down.
def dyn_p(p): return shift_params(p, dL=-0.02, dE=-0.02, bE=-0.1)
def dyn_d(V,A): return delta_basic(V,A)
def dyn_pol(z,V,A): return 'INTERPRET' if (z.R>0.6 and z.E>0.6) else 'NONE'

# 4. Attachment Theory
# Focus: Secure Base. Love (L) regulates Exploration (C) and Fear (E).
def att_p(p): return shift_params(p, bC=+0.1, bR=+0.1, aE=-0.2)
def att_d(V,A): return 0.85 * delta_basic(V,A)
def att_pol(z,V,A): return 'RELATEDNESS' if z.R > 0.6 else 'NONE'

# 5. Mindfulness / Compassion
# Focus: Non-reactivity. Ego (E) suppression, high Love (L).
def min_p(p): return shift_params(p, aE=-0.2, dE=+0.1, bE=+0.1)
def min_d(V,A): return 0.80 * delta_basic(V,A)
def min_pol(z,V,A): return 'BREATH' if z.E>0.6 else ('COMPASSION' if z.R>0.6 else 'NONE')

# 6. Behavioral / RL
# Focus: Exposure. High Control (C), driven by Arousal.
def beh_p(p): return shift_params(p, aC=+0.2, bC=+0.1)
def beh_d(V,A): return 0.95 * (1.0*A - 0.4*V) 
def beh_pol(z,V,A): return 'EXPOSURE' if z.E > 0.7 else 'NONE'

# 7. Predictive Processing
# Focus: Error Minimization. Very sensitive to R (Prediction Error).
def pp_p(p): return shift_params(p, aR=+0.2, bR=+0.1, aL=+0.1)
def pp_d(V,A): return clamp(1.1*A - 0.8*V, -1.5, 1.5)
def pp_pol(z,V,A): return 'REAPPRAISE' if z.R > 0.8 else 'NONE'

# 8. SDT (Self-Determination Theory)
# Focus: Autonomy/Competence (C) and Relatedness (L).
def sdt_p(p): return shift_params(p, aC=+0.2, bC=+0.1)
def sdt_d(V,A): return 0.90 * delta_basic(V,A)
def sdt_pol(z,V,A): return 'AUTONOMY' if z.C < 0.5 else 'NONE'


SCHOOLS = [
    SchoolSpec('CBT', cbt_p, cbt_d, cbt_pol),
    SchoolSpec('ACT', act_p, act_d, act_pol),
    SchoolSpec('Psychodynamic', dyn_p, dyn_d, dyn_pol),
    SchoolSpec('Attachment', att_p, att_d, att_pol),
    SchoolSpec('Mindfulness', min_p, min_d, min_pol),
    SchoolSpec('Behavioral_RL', beh_p, beh_d, beh_pol),
    SchoolSpec('PredictiveProcessing', pp_p, pp_d, pp_pol),
    SchoolSpec('SDT', sdt_p, sdt_d, sdt_pol),
]

# ==========================================
# 2) Digital Twin Engine
# ==========================================

class DigitalTwin:
    def __init__(self, school_name='CBT'):
        spec = next((s for s in SCHOOLS if s.name == school_name), SCHOOLS[0])
        self.spec = spec
        base_p = Params()
        self.state = RLEC(p=spec.param_shifter(base_p))
        self.history = []

    def step(self, V, A, turn_idx=0):
        # 1. Calc Delta (School-specific perception)
        raw_delta = self.spec.delta_func(V, A)
        
        # 2. Policy (Ritual Decision)
        ritual_name = self.spec.policy_func(self.state, V, A)
        eff = RITUALS.get(ritual_name, RITUALS['NONE'])
        
        # 3. Apply Intervention (Right-Brain DSL)
        eff_delta = raw_delta * eff['d_scale']
        
        # 4. ODE Step (Time Evolution)
        self.state.step(eff_delta, uL=eff['uL'], uC=eff['uC'], uE=eff['uE'])
        
        # 5. Observe
        V_out, A_out = self.state.observe()
        
        log = {
            'Turn': turn_idx,
            'School': self.spec.name,
            'V_in': round(V,2), 'A_in': round(A,2), 
            'Delta': round(eff_delta,2),
            'Ritual': ritual_name,
            'R': round(self.state.R,3), 'L': round(self.state.L,3),
            'E': round(self.state.E,3), 'C': round(self.state.C,3),
            'V_out': round(V_out,2), 'A_out': round(A_out,2)
        }
        self.history.append(log)
        return log

    def save_csv(self, filename):
        if not self.history: return
        keys = self.history[0].keys()
        with open(filename, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(self.history)
            
    def plot_history(self, filename):
        turns = [x['Turn'] for x in self.history]
        Rs = [x['R'] for x in self.history]
        Ls = [x['L'] for x in self.history]
        Es = [x['E'] for x in self.history]
        Cs = [x['C'] for x in self.history]
        Deltas = [x['Delta'] for x in self.history]
        
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(turns, Rs, label='R (Resistance)', color='red', linewidth=2)
        ax.plot(turns, Ls, label='L (Love)', color='green', linewidth=2)
        ax.plot(turns, Es, label='E (Ego)', color='purple', linewidth=2)
        ax.plot(turns, Cs, label='C (Control)', color='blue', linewidth=2)
        ax.bar(turns, Deltas, alpha=0.15, color='gray', label='Delta (Input)')
        
        # Mark rituals
        for x in self.history:
            if x['Ritual'] != 'NONE':
                ax.axvline(x['Turn'], color='orange', linestyle=':', alpha=0.6)
                ax.text(x['Turn'], 2.5, x['Ritual'], rotation=90, fontsize=8, color='orange', ha='right')

        ax.set_title(f"Love-OS Dynamics: {self.spec.name} Model")
        ax.set_ylim(-2.5, 3.5)
        ax.set_xlabel("Time (Turns)")
        ax.set_ylabel("Internal State (z)")
        ax.legend(loc='upper left')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

# ==========================================
# 3) Main: Run All Schools
# ==========================================
if __name__ == "__main__":
    # Scenario: Calm -> Shock -> Stress -> Recovery
    # (Valence, Arousal) sequence
    SCENARIO = [
        (0.1, 0.2),  # 0: Calm
        (-0.8, 0.9), # 1: Shock (Insult)
        (-0.5, 0.8), # 2: Stress
        (-0.4, 0.7), # 3: Sustained Stress
        (0.0, 0.5),  # 4: Neutral
        (0.3, 0.4),  # 5: Recovery
        (0.6, 0.2),  # 6: Joy
        (0.2, 0.1),  # 7: Calm
    ]

    print("--- Running Love-OS Unified Psychology Simulation ---")
    for school in SCHOOLS:
        twin = DigitalTwin(school.name)
        print(f"Simulating: {school.name}...")
        for i, (v, a) in enumerate(SCENARIO):
            twin.step(v, a, turn_idx=i)
        
        csv_name = f"schools_{school.name}.csv"
        png_name = f"schools_{school.name}.png"
        twin.save_csv(csv_name)
        twin.plot_history(png_name)
        print(f"  -> Saved {csv_name} & {png_name}")
    print("\nAll schools simulated. The Grand Unification is complete.")
