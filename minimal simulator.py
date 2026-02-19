import numpy as np

import matplotlib.pyplot as plt

# =====================

# Love-OS minimal simulator (complex amplitude + Landau order + phase lock)

# =====================

# ---- Parameters (feel free to tweak) ----

T = 200.0            # total time

dt = 0.02            # step

# Hopf normal form (virtual side)

omega = 0.6          # natural phase drift (old environment)

mu0   = -0.2         # initial control param (below threshold)

ramp  = 0.004        # mu increases linearly: mu(t) = mu0 + ramp*t

beta  = 0.6          # amplitude saturation (real part)

gamma = 0.3          # amplitude-phase coupling (imaginary)

# Phase locking to North Star theta0

theta0 = np.pi       # North Star (opposite direction to the ego forward)

K0     = 0.5         # coupling gain factor -> K(R) = K0 * R

# Landau potential for the real side (reality)

alpha = 1.0

Rc    = 0.9          # critical R at which a(R) changes sign

b     = 1.0

c     = 0.8          # coupling from phase to reality via sin(theta-theta0)

# Initial states

R = 0.05

th = 0.0

X = 0.0

n = int(T/dt)

# Storage

Ts = np.linspace(0, T, n+1)

R_hist = np.zeros(n+1)

th_hist = np.zeros(n+1)

X_hist = np.zeros(n+1)

Z_hist = np.zeros(n+1)

mu_hist = np.zeros(n+1)

K_hist = np.zeros(n+1)

a_hist = np.zeros(n+1)

lock_hist = np.zeros(n+1, dtype=bool)

R_hist[0], th_hist[0], X_hist[0] = R, th, X

mu_hist[0] = mu0 + ramp*0

K_hist[0] = K0*R

Z_hist[0] = np.abs(np.exp(1j*th)+1)

a_hist[0] = alpha*(Rc - R)

lock_hist[0] = (abs(omega) <= K_hist[0])

# ---- Dynamics (RK4) ----

def deriv(state, t):

    R, th, X = state

    mu = mu0 + ramp*t

    # Amplitude-phase equations (polar Hopf with phase-coupling)

    dR = mu*R - beta*R**3

    K = K0 * R

    dth = omega - gamma*R**2 - K*np.sin(th - theta0)

    # Landau order parameter

    aR = alpha*(Rc - R)

    dX = -(aR*X + b*X**3) - c*np.sin(th - theta0)

    return np.array([dR, dth, dX])

state = np.array([R, th, X], dtype=float)

for i in range(1, n+1):

    t = Ts[i-1]

    k1 = deriv(state, t)

    k2 = deriv(state + 0.5*dt*k1, t + 0.5*dt)

    k3 = deriv(state + 0.5*dt*k2, t + 0.5*dt)

    k4 = deriv(state + dt*k3, t + dt)

    state = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

    # unwrap theta for continuity (optional)

    state[1] = np.angle(np.exp(1j*state[1]))  # keep within (-pi, pi]

    R, th, X = state

    R_hist[i] = R

    th_hist[i] = th

    X_hist[i] = X

    mu_hist[i] = mu0 + ramp*Ts[i]

    K_hist[i] = K0*R

    Z_hist[i] = np.abs(np.exp(1j*th)+1)

    a_hist[i] = alpha*(Rc - R)

    lock_hist[i] = (abs(omega) <= K_hist[i])

# ---- Key events (crossings) ----

# time when mu crosses zero (Hopf threshold)

try:

    idx_mu = np.where(mu_hist>=0)[0][0]

except IndexError:

    idx_mu = None

# time when R passes Rc (Landau threshold)

try:

    idx_Rc = np.where(R_hist>=Rc)[0][0]

except IndexError:

    idx_Rc = None

# time when locking condition |omega|<=K(R) becomes true

try:

    idx_lock = np.where(lock_hist)[0][0]

except IndexError:

    idx_lock = None

# ---- Plotting ----

plt.style.use('seaborn-v0_8-darkgrid')

fig, axes = plt.subplots(4,1, figsize=(10,12), sharex=True)

axes[0].plot(Ts, mu_hist, label='mu(t)')

axes[0].axhline(0, color='k', lw=1)

if idx_mu is not None:

    axes[0].axvline(Ts[idx_mu], color='r', ls='--', lw=1)

    axes[0].annotate('Hopf threshold (mu=0)', xy=(Ts[idx_mu],0), xytext=(Ts[idx_mu]+5,0.2),

                     arrowprops=dict(arrowstyle='->'))

axes[0].set_ylabel('mu')

axes[0].legend(loc='upper left')

axes[1].plot(Ts, R_hist, label='R(t) = |A| (virtual amplitude)')

axes[1].axhline(Rc, color='purple', ls='--', lw=1, label='Rc (Landau)')

if idx_Rc is not None:

    axes[1].axvline(Ts[idx_Rc], color='purple', ls='--', lw=1)

    axes[1].annotate('R crosses Rc', xy=(Ts[idx_Rc], Rc), xytext=(Ts[idx_Rc]+5, Rc+0.2),

                     arrowprops=dict(arrowstyle='->'))

axes[1].set_ylabel('R (virtual)')

axes[1].legend(loc='upper left')

axes[2].plot(Ts, X_hist, label='X(t) (reality order)')

axes[2].axhline(0, color='k', lw=1)

axes[2].set_ylabel('X (real)')

axes[2].legend(loc='upper left')

axes[3].plot(Ts, th_hist, label='theta (phase)')

axes[3].plot(Ts, Z_hist, label='Z = |e^{i theta}+1|')

axes[3].axhline(np.pi, color='gray', ls='--', lw=1, label='pi')

axes[3].axhline(0, color='k', lw=1)

if idx_lock is not None:

    axes[3].axvline(Ts[idx_lock], color='g', ls='--', lw=1)

    axes[3].annotate('phase lock (|omega|<=K(R))', xy=(Ts[idx_lock], th_hist[idx_lock]),

                     xytext=(Ts[idx_lock]+5, th_hist[idx_lock]+0.8),

                     arrowprops=dict(arrowstyle='->'))

axes[3].set_xlabel('time')

axes[3].legend(loc='upper right')

fig.suptitle('Love-OS Minimal Simulation: Virtual → Phase Lock → Reality Emergence', fontsize=14)

fig.tight_layout(rect=[0,0,1,0.97])

fig.savefig('love_os_minimal_simulation_timeseries.png', dpi=160)

# Phase portrait

fig2, ax2 = plt.subplots(1,2, figsize=(12,5))

ax2[0].plot(R_hist, X_hist, color='teal')

ax2[0].axvline(Rc, color='purple', ls='--', lw=1)

ax2[0].set_xlabel('R (virtual)')

ax2[0].set_ylabel('X (real)')

ax2[0].set_title('Phase portrait: R vs X')

ax2[1].plot(Ts, K_hist, label='K(R)')

ax2[1].axhline(abs(omega), color='orange', ls='--', lw=1, label='|omega|')

ax2[1].set_xlabel('time')

ax2[1].set_ylabel('K and |omega|')

ax2[1].legend()

ax2[1].set_title('Locking condition: |omega| ≤ K(R)')

fig2.tight_layout()

fig2.savefig('love_os_minimal_simulation_phase.png', dpi=160)

print({'files':['love_os_minimal_simulation_timeseries.png','love_os_minimal_simulation_phase.png'],

       'mu_cross_time': float(Ts[idx_mu]) if idx_mu is not None else None,

       'R_cross_time': float(Ts[idx_Rc]) if idx_Rc is not None else None,

       'lock_time': float(Ts[idx_lock]) if idx_lock is not None else None})
