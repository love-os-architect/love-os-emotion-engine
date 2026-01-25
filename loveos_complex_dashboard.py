"""
Love-OS Complex Dashboard — amplitude / phase / synchrony (v0.1)
----------------------------------------------------------------
- Complex-order-parameter version of Love-OS using two complex oscillators:
    psi1 = (L - R) + i E
    psi2 = C + i A   (A can be treated as arousal proxy)

- Stuart–Landau-type ODE with optional coupling between two agents (self, other):
    dpsi/dt = (sigma + i*omega)*psi - (kappa + i*eta)*|psi|^2*psi + Gamma*Delta + U + Coupling

- Rituals (BREATH, LABEL, REAPPRAISE, COMPASSION) map to small parameter nudges for a duration.
- Dashboard plots (time series): |psi1|, |psi2|, phases arg(psi1/psi2), Kuramoto R, Valence/Arousal.

Run modes:
  1) Headless demo (default here): simulates and saves PNG + CSV.
  2) Live mode (if you run locally): add flag --live to open an interactive window.

Usage:
  python loveos_complex_dashboard.py            # headless demo, saves files
  python loveos_complex_dashboard.py --live     # interactive window (matplotlib)
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Complex ODE core
# ------------------------------
class ComplexAgent:
    def __init__(self, name='self',
                 psi1=0.2+0.1j, psi2=0.2+0.0j,
                 # base params (can be tuned / learned)
                 sigma1=0.20, omega1=2.0, kappa1=0.30, eta1=0.10,
                 sigma2=0.10, omega2=1.2, kappa2=0.20, eta2=0.05,
                 Gamma1=0.5+0.0j, Gamma2=0.3+0.0j):
        self.name = name
        self.psi1 = complex(psi1)
        self.psi2 = complex(psi2)
        self.params = dict(
            sigma1=sigma1, omega1=omega1, kappa1=kappa1, eta1=eta1,
            sigma2=sigma2, omega2=omega2, kappa2=kappa2, eta2=eta2,
            Gamma1=Gamma1, Gamma2=Gamma2
        )
        # Active ritual schedule: list of (t_end, effect_dict)
        self.active_effects = []

    def _params_with_effects(self, t):
        p = self.params.copy()
        # apply active effects whose t_end >= t
        new_active = []
        for t_end, eff in self.active_effects:
            if t <= t_end:
                for k,v in eff.items():
                    p[k] = p.get(k,0) + v
                new_active.append((t_end, eff))
        self.active_effects = new_active
        return p

    def ritual(self, name: str, t: float, duration: float=8.0):
        """Schedule a ritual effect lasting `duration` seconds."""
        name = name.upper()
        eff = {}
        if name == 'BREATH':
            # calm rotation and phase twist
            eff = {'omega1': -0.6, 'omega2': -0.4, 'eta1': -0.05, 'eta2': -0.03}
        elif name == 'LABEL':
            # enhance integration gain
            eff = {'sigma1': +0.15}
        elif name in ('REAPPRAISE','CBT'):
            # increase integration + mild saturation to avoid overshoot
            eff = {'sigma1': +0.12, 'kappa1': +0.08, 'eta1': -0.02}
        elif name == 'COMPASSION':
            # align rhythms and soften phase nonlinearity
            eff = {'omega1': -0.3, 'eta1': -0.06}
        elif name == 'AUTONOMY':
            eff = {'sigma2': +0.12}
        else:
            return
        self.active_effects.append((t + duration, eff))

    def step(self, dt: float, Delta: float, other: 'ComplexAgent|None'=None, K: float=0.0):
        p = self.params
        # include time-varying effects in derivative computation by reading applied deltas
        # For stability, use small dt (e.g., 0.02)
        def deriv(psi, sigma, omega, kappa, eta, Gamma, D, U=0+0j, psi_other=None, K=0.0):
            coup = 0.0+0.0j
            if psi_other is not None and K != 0.0:
                # diffusive complex coupling (align amplitude+phase)
                coup = K*(psi_other - psi)
            return (sigma + 1j*omega)*psi - (kappa + 1j*eta)*abs(psi)**2*psi + Gamma*D + U + coup

        # pull dynamic params with current effects (approx by midpoint rule)
        cur = self._params_with_effects(t=0.0)  # effects already filtered per call site
        # compute derivatives
        psi1_other = other.psi1 if other is not None else None
        d1 = deriv(self.psi1, cur['sigma1'], cur['omega1'], cur['kappa1'], cur['eta1'], cur['Gamma1'], Delta,
                   psi_other=psi1_other, K=K)
        psi2_other = other.psi2 if other is not None else None
        d2 = deriv(self.psi2, cur['sigma2'], cur['omega2'], cur['kappa2'], cur['eta2'], cur['Gamma2'], Delta*0.6,
                   psi_other=psi2_other, K=0.5*K)

        self.psi1 += dt * d1
        self.psi2 += dt * d2

    # Readouts
    @property
    def L_minus_R(self):
        return self.psi1.real
    @property
    def E(self):
        return self.psi1.imag
    @property
    def C(self):
        return self.psi2.real
    @property
    def A(self):
        return abs(self.psi2)
    def valence(self):
        # V = tanh(a1*Re(psi1) + a2*Re(psi2) - a3*Im(psi1))
        return np.tanh(1.0*self.psi1.real + 0.6*self.psi2.real - 0.8*self.psi1.imag)

# ------------------------------
# Simulation driver
# ------------------------------

def simulate(T=60.0, dt=0.02, K=0.15, schedule=None, headless=True, out_png='complex_dashboard_demo.png', out_csv='complex_dashboard_demo.csv'):
    N = int(T/dt)
    t = np.arange(N)*dt
    me = ComplexAgent('self')
    you = ComplexAgent('other', psi1=0.15+0.05j, psi2=0.15+0.0j, omega1=1.8, omega2=1.1)

    # default schedule: stress pulses and rituals
    schedule = schedule or [
        {'t0':10,'t1':20,'type':'stress','amp':+1.0},
        {'t0':20,'t1':28,'type':'ritual','name':'BREATH','who':'self'},
        {'t0':35,'t1':45,'type':'stress','amp':+0.9},
        {'t0':45,'t1':54,'type':'ritual','name':'LABEL','who':'self'},
    ]

    # allocate
    rec = {
        't': t,
        'psi1_abs_self': np.zeros(N), 'psi2_abs_self': np.zeros(N),
        'phi1_self': np.zeros(N), 'phi2_self': np.zeros(N),
        'V_self': np.zeros(N), 'A_self': np.zeros(N),
        'psi1_abs_other': np.zeros(N), 'psi2_abs_other': np.zeros(N),
        'phi1_other': np.zeros(N), 'phi2_other': np.zeros(N),
        'V_other': np.zeros(N), 'A_other': np.zeros(N),
        'Delta': np.zeros(N), 'R_kuramoto': np.zeros(N),
    }

    # helper for Delta
    def Delta_at(time_s):
        d = 0.0
        for ev in schedule:
            if ev['type']=='stress' and ev['t0'] <= time_s < ev['t1']:
                d += ev.get('amp',1.0)
        return d

    # simulate
    for i,ti in enumerate(t):
        # apply rituals when entering their window
        for ev in schedule:
            if ev['type']=='ritual' and abs(ti-ev['t0'])<1e-9:  # start
                who = me if ev.get('who','self')=='self' else you
                who.ritual(ev['name'], t=ti, duration=(ev['t1']-ev['t0']))
        D = Delta_at(ti)
        me.step(dt, D, other=you, K=K)
        you.step(dt, D*0.7, other=me, K=K*0.8)  # other perceives slightly attenuated stress

        # record
        rec['psi1_abs_self'][i] = abs(me.psi1)
        rec['psi2_abs_self'][i] = abs(me.psi2)
        rec['phi1_self'][i] = np.angle(me.psi1)
        rec['phi2_self'][i] = np.angle(me.psi2)
        rec['V_self'][i] = me.valence()
        rec['A_self'][i] = me.A

        rec['psi1_abs_other'][i] = abs(you.psi1)
        rec['psi2_abs_other'][i] = abs(you.psi2)
        rec['phi1_other'][i] = np.angle(you.psi1)
        rec['phi2_other'][i] = np.angle(you.psi2)
        rec['V_other'][i] = you.valence()
        rec['A_other'][i] = you.A

        rec['Delta'][i] = D
        # Kuramoto order parameter for psi1 phases (two agents)
        z = np.exp(1j*rec['phi1_self'][i]) + np.exp(1j*rec['phi1_other'][i])
        rec['R_kuramoto'][i] = np.abs(z/2.0)

    # save CSV
    df = pd.DataFrame(rec)
    df.to_csv(out_csv, index=False)

    # plotting dashboard
    fig = plt.figure(figsize=(12,8))
    gs = fig.add_gridspec(2,2)

    # (1) Amplitude
    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(t, rec['psi1_abs_self'], label='|psi1| self', color='#2ca02c')
    ax1.plot(t, rec['psi1_abs_other'], label='|psi1| other', color='#98df8a')
    ax1.plot(t, rec['psi2_abs_self'], label='|psi2| self', color='#1f77b4')
    ax1.plot(t, rec['psi2_abs_other'], label='|psi2| other', color='#aec7e8')
    ax1.set_title('Amplitude (Integration/Ego & Control/Arousal)')
    ax1.set_ylabel('Amplitude')
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    # (2) Phase (wrapped)
    ax2 = fig.add_subplot(gs[0,1])
    ax2.plot(t, rec['phi1_self'], label='phase psi1 self', color='#d62728')
    ax2.plot(t, rec['phi1_other'], label='phase psi1 other', color='#ff9896')
    ax2.set_title('Phase (psi1)'); ax2.set_ylabel('rad')
    ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

    # (3) Kuramoto R and Delta
    ax3 = fig.add_subplot(gs[1,0])
    ax3.plot(t, rec['R_kuramoto'], label='Kuramoto R (sync)', color='#bcbd22')
    ax3.step(t, rec['Delta']/max(1.0, np.max(rec['Delta'])), where='mid', label='Delta (scaled)', color='black')
    ax3.set_title('Synchrony & Stress'); ax3.set_ylabel('R / scaled Δ'); ax3.set_xlabel('time [s]')
    ax3.legend(fontsize=8); ax3.grid(alpha=0.3)

    # (4) Valence & Arousal (self)
    ax4 = fig.add_subplot(gs[1,1])
    ax4.plot(t, rec['V_self'], label='Valence self', color='#17becf')
    ax4.plot(t, rec['A_self']/max(1e-6, np.max(rec['A_self'])), label='Arousal self (scaled)', color='#7f7f7f')
    ax4.set_title('Valence & Arousal (self)'); ax4.set_xlabel('time [s]')
    ax4.legend(fontsize=8); ax4.grid(alpha=0.3)

    fig.suptitle('Love-OS Complex Digital Twin — Amplitude / Phase / Synchrony', fontsize=12)
    fig.tight_layout(rect=[0,0,1,0.96])
    fig.savefig(out_png, dpi=160)

    return out_png, out_csv

# ------------------------------
# Live mode (matplotlib animation) — optional
# ------------------------------

def live_mode():
    import matplotlib.animation as animation

    T, dt = 60.0, 0.02
    N = int(T/dt)
    t = np.arange(N)*dt
    me = ComplexAgent('self')
    you = ComplexAgent('other', psi1=0.15+0.05j, psi2=0.15+0.0j, omega1=1.8, omega2=1.1)
    schedule = [
        {'t0':10,'t1':20,'type':'stress','amp':+1.0},
        {'t0':20,'t1':28,'type':'ritual','name':'BREATH','who':'self'},
        {'t0':35,'t1':45,'type':'stress','amp':+0.9},
        {'t0':45,'t1':54,'type':'ritual','name':'LABEL','who':'self'},
    ]

    def Delta_at(ts):
        d=0.0
        for ev in schedule:
            if ev['type']=='stress' and ev['t0']<=ts<ev['t1']:
                d+=ev.get('amp',1.0)
        return d

    fig, axes = plt.subplots(2,2, figsize=(12,8))
    ax1, ax2, ax3, ax4 = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # Prepare lines
    l11, = ax1.plot([], [], label='|psi1| self', color='#2ca02c')
    l12, = ax1.plot([], [], label='|psi1| other', color='#98df8a')
    l13, = ax1.plot([], [], label='|psi2| self', color='#1f77b4')
    l14, = ax1.plot([], [], label='|psi2| other', color='#aec7e8')
    ax1.set_xlim(0, T); ax1.set_ylim(0, 2.0); ax1.set_title('Amplitude'); ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    l21, = ax2.plot([], [], label='phase psi1 self', color='#d62728')
    l22, = ax2.plot([], [], label='phase psi1 other', color='#ff9896')
    ax2.set_xlim(0, T); ax2.set_ylim(-np.pi, np.pi); ax2.set_title('Phase (psi1)'); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

    l31, = ax3.plot([], [], label='Kuramoto R', color='#bcbd22')
    l32, = ax3.plot([], [], label='Delta (scaled)', color='black')
    ax3.set_xlim(0, T); ax3.set_ylim(0, 1.2); ax3.set_title('Synchrony & Stress'); ax3.legend(fontsize=8); ax3.grid(alpha=0.3)

    l41, = ax4.plot([], [], label='Valence self', color='#17becf')
    l42, = ax4.plot([], [], label='Arousal self (scaled)', color='#7f7f7f')
    ax4.set_xlim(0, T); ax4.set_ylim(-1.1, 1.1); ax4.set_title('Valence & Arousal (self)'); ax4.legend(fontsize=8); ax4.grid(alpha=0.3)

    # Buffers
    y11=[]; y12=[]; y13=[]; y14=[]
    y21=[]; y22=[]
    y31=[]; y32=[]
    y41=[]; y42=[]

    # schedule rituals at t0
    ev_seen=set()

    def animate(frame):
        ts = frame*dt
        for ev in schedule:
            if ev['type']=='ritual' and ev['t0']<=ts<ev['t0']+dt and (id(ev) not in ev_seen):
                who = me if ev.get('who','self')=='self' else you
                who.ritual(ev['name'], t=ts, duration=(ev['t1']-ev['t0']))
                ev_seen.add(id(ev))
        D = Delta_at(ts)
        me.step(dt, D, other=you, K=0.15)
        you.step(dt, D*0.7, other=me, K=0.12)

        # append buffers
        y11.append(abs(me.psi1)); y12.append(abs(you.psi1)); y13.append(abs(me.psi2)); y14.append(abs(you.psi2))
        y21.append(np.angle(me.psi1)); y22.append(np.angle(you.psi1))
        Rkur = np.abs((np.exp(1j*y21[-1]) + np.exp(1j*y22[-1]))/2.0)
        y31.append(Rkur); y32.append(D)
        V = np.tanh(1.0*me.psi1.real + 0.6*me.psi2.real - 0.8*me.psi1.imag)
        A = abs(me.psi2); y41.append(V); y42.append(A/max(1e-6, 2.0))

        X = np.arange(len(y11))*dt
        l11.set_data(X, y11); l12.set_data(X, y12); l13.set_data(X, y13); l14.set_data(X, y14)
        l21.set_data(X, y21); l22.set_data(X, y22)
        l31.set_data(X, y31); l32.set_data(X, np.array(y32)/max(1.0, np.max(y32)))
        l41.set_data(X, y41); l42.set_data(X, np.array(y42))
        return l11,l12,l13,l14,l21,l22,l31,l32,l41,l42

    ani = animation.FuncAnimation(fig, animate, frames=N, interval=20, blit=False, repeat=False)
    fig.tight_layout()
    plt.show()

# ------------------------------
# Main
# ------------------------------
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true', help='Run interactive matplotlib animation window')
    args = ap.parse_args()
    if args.live:
        live_mode()
    else:
        png, csv = simulate()
        print('Saved:', png, csv)
