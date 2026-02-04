import os

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime, timedelta

# 1) Load existing CSV if available; otherwise, synthesize the same structure

csv_path = 'loveos_demo_21days.csv'

if os.path.exists(csv_path):

    df = pd.read_csv(csv_path)

    df['date_dt'] = pd.to_datetime(df['date'])

else:

    # fallback: build synthetic data similar to before

    np.random.seed(42)

    DAYS = 21

    start = datetime.today() - timedelta(days=DAYS-1)

    dates = [start + timedelta(days=i) for i in range(DAYS)]

    phase, m_vals, C_vals, R_vals = [], [], [], []

    for i in range(DAYS):

        if i < 7: p = 'baseline'

        elif i < 14: p = 'intervention'

        else: p = 'washout'

        phase.append(p)

        base_m = 4 + 0.2*np.random.randn()

        base_C = 3 + 0.5*np.random.randn()

        base_R = 0.45 + 0.05*np.random.randn()

        if p == 'intervention':

            base_m += 1.2; base_C -= 0.8; base_R += 0.2

        if p == 'washout':

            base_m += 0.3; base_C -= 0.2; base_R += 0.05

        m_vals.append(np.clip(base_m,1,7))

        C_vals.append(np.clip(base_C,0,7))

        R_vals.append(np.clip(base_R,0,1))

    m_bar = np.array(m_vals); C_bar = np.array(C_vals); R = np.array(R_vals)

    alpha0, aR, aC, aM = 1.0, 1.2, 0.2, 0.25

    tau_dot = (alpha0 + aR*R)*(1 - aC*C_bar/7.0)*(1 + aM*m_bar/7.0)

    E = 1.0 + 0.1*np.random.randn(DAYS)

    W = 1/(1+np.exp(-(0.9*m_bar - 0.6*C_bar)))

    v = (0.9*E*R*W - 0.1) + 0.05*np.random.randn(DAYS)

    df = pd.DataFrame({

        'date':[d.date().isoformat() for d in dates],

        'phase':phase,

        'subjective_time_density_index':np.round(tau_dot,3),

        'progress_speed_index':np.round(v,3)

    })

    df['date_dt'] = pd.to_datetime(df['date'])

# 2) Create English plot without Japanese text

plt.rcParams.update({

    'font.family':'DejaVu Sans',  # English-capable default

    'axes.unicode_minus': False

})

x = df['date_dt']

_tau = df['subjective_time_density_index']

_v = df['progress_speed_index']

phases = df['phase'].tolist()

fig, ax = plt.subplots(figsize=(11.5,6.2))

ax.plot(x, _tau, label='Subjective time density (τ̇ index)', color='#1f77b4', lw=2)

ax.plot(x, _v, label='Meaning-aligned speed (v∥ index)', color='#ff7f0e', lw=2)

# Phase shading with English labels

for p, color, label in [

    ('baseline', '#d3d3d345', 'Baseline'),

    ('intervention', '#2ca02c25', 'Intervention'),

    ('washout', '#9467bd25', 'Washout'),

]:

    idx = [i for i,ph in enumerate(phases) if ph==p]

    if idx:

        x0 = x.min() if min(idx)==0 else x[min(idx)]

        x1 = x.max() if max(idx)==len(x)-1 else x[max(idx)]

        ax.axvspan(x0, x1, color=color)

        xm = x[(min(idx)+max(idx))//2]

        ymax = max(_tau.max(), _v.max())

        ax.text(xm, ymax*1.02, label, ha='center', va='bottom', fontsize=10)

ax.set_title('Change in subjective time density and action speed by mindset (demo)', fontsize=14)

ax.set_xlabel('Date')

ax.set_ylabel('Normalized index')

ax.grid(True, alpha=0.3)

ax.legend()

fig.tight_layout()

out_path = 'loveos_time_perception_en.png'

fig.savefig(out_path, dpi=160)

print('Saved', out_path)

