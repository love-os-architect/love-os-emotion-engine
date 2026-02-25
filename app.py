mport streamlit as st

import numpy as np

import matplotlib.pyplot as plt

st.set_page_config(page_title="Love-OS Dashboard V2.0", layout="wide")

# ==========================================

# 1. UI: Sidebar (Y-Intention & Z-Power)

# ==========================================

st.sidebar.title("Love-OS Core (Cubic)")

st.sidebar.markdown("### Observable Inputs")

y_intention = st.sidebar.slider(

    "Intention Y (Phase Alignment)", 

    0.0, 2.0, 1.0, 0.1, 

    help="Quality of surrender, resonance, and alignment."

)

z_power = st.sidebar.slider(

    "Power Z (Energy/Agency)", 

    0.0, 2.0, 0.5, 0.1, 

    help="Active energy, volume of action, and participation."

)

chi_alignment = st.sidebar.slider("Alignment χ (Y-Z Consistency)", 0.0, 1.0, 0.8)

st.sidebar.markdown("### System Constants")

beta_gain = st.sidebar.slider("Linear Gain Coef", 0.0, 1.0, 0.5)

c2_nonlin = st.sidebar.slider("Cubic Non-linearity (c2)", 0.0, 5.0, 1.0)

if st.sidebar.button("🚨 /phase-shift (Bifurcation Reset)"):

    st.session_state['phase_shift'] = True

else:

    st.session_state['phase_shift'] = False

# ==========================================

# 2. Core Logic (Stuart-Landau / Cubic Model)

# ==========================================

def run_stuart_landau_sim(Y, Z, chi, c2, phase_shift):

    dt = 0.05

    steps = 600

    time = np.linspace(0, steps*dt, steps)

    

    # State: W = R * exp(i*theta)

    # Using 2 nodes (A and B)

    W_A = 0.1 + 0j

    W_B = -0.1 + 0j # Opposite phase

    

    omega_A, omega_B = 1.0, 1.1 # Natural frequencies

    

    # Results history

    r_hist, q_hist, amp_hist = np.zeros(steps), np.zeros(steps), np.zeros(steps)

    thA_hist, thB_hist = np.zeros(steps), np.zeros(steps)

    

    # Effective gain mu based on Y, Z, and alignment chi

    mu = (Y + Z * chi) * 0.5 

    K = 1.5 * (Y * Z) # Coupling driven by both

    

    # Reset via Phase Shift

    if phase_shift:

        W_B = W_A * 1.1 # Force alignment

        mu += 1.0 # Temporary boost to cross bifurcation point

    

    q_accum = 0.0

    

    for i in range(steps):

        # Stuart-Landau Equation (Cubic non-linearity)

        # dW/dt = (mu + i*omega)*W - (1 + i*c2)*|W|^2*W + Coupling

        

        # Node A

        coupling_A = K * (W_B - W_A)

        dW_A = (mu + 1j*omega_A)*W_A - (1 + 1j*c2)*(np.abs(W_A)**2)*W_A + coupling_A

        W_A += dW_A * dt

        

        # Node B

        coupling_B = K * (W_A - W_B)

        dW_B = (mu + 1j*omega_B)*W_B - (1 + 1j*c2)*(np.abs(W_B)**2)*W_B + coupling_B

        W_B += dW_B * dt

        

        # Metrics

        z_combined = (W_A + W_B) / 2

        r = np.abs(z_combined) # Coherence

        res_R = 2.0 * np.exp(-0.5 * np.abs(W_A + W_B)) # Resistance drops as they sync

        q_accum += res_R * dt

        

        # Store

        r_hist[i] = r

        q_hist[i] = q_accum

        amp_hist[i] = np.abs(W_A)

        thA_hist[i] = np.angle(W_A)

        thB_hist[i] = np.angle(W_B)

        

    return time, r_hist, q_hist, amp_hist, thA_hist, thB_hist

# Execute

time, r, q, amp, thA, thB = run_stuart_landau_sim(y_intention, z_power, chi_alignment, c2_nonlin, st.session_state['phase_shift'])

# ==========================================

# 3. UI: Dashboard View

# ==========================================

st.title("Love-OS: Phase-Power (Cubic) Dashboard")

st.markdown("Visualizing the **Phase Transition** to Social Superconductivity using **Stuart-Landau (Cubic Non-linear)** Dynamics.")

m1, m2, m3 = st.columns(3)

m1.metric("Order Parameter (r)", f"{r[-1]:.3f}", f"{r[-1]-r[0]:.3f}")

m2.metric("System Amplitude (Z-Power)", f"{amp[-1]:.3f}")

m3.metric("Dissipation (Q)", f"{q[-1]:.2f}", delta_color="inverse")

# Branch/Bifurcation Status

if r[-1] < 0.3:

    st.warning("📉 **Low Order State:** Insufficient Y-Z alignment. The system is stuck in the 'Zero-Branch'. Increase Power or Intention.")

elif r[-1] > 0.8:

    st.success("🚀 **Lock-in Achieved:** The system has jumped to the High-Order Branch (Superconductivity).")

# Visuals

c_l, c_r = st.columns(2)

with c_l:

    st.subheader("Bifurcation & Synchronization (r)")

    fig1, ax1 = plt.subplots()

    ax1.plot(time, r, label="Order Parameter (r)", color="purple", lw=3)

    ax1.fill_between(time, 0, r, color="purple", alpha=0.1)

    ax1.set_ylim(0, 1.1)

    ax1.set_xlabel("Time")

    ax1.legend()

    st.pyplot(fig1)

with c_r:

    st.subheader("Cubic Self-Regulation (Amplitude & Phase)")

    fig2, ax2 = plt.subplots()

    ax2.plot(time, np.sin(thA), label="Phase A (sin θ)", alpha=0.6)

    ax2.plot(time, np.sin(thB), label="Phase B (sin θ)", alpha=0.6)

    ax2_twin = ax2.twinx()

    ax2_twin.plot(time, q, color="red", label="Dissipation (Q)", lw=2)

    ax2.set_xlabel("Time")

    ax2.legend(loc="upper left")

    ax2_twin.legend(loc="lower right")

    st.pyplot(fig2)

st.info("**Core Insight:** The cubic term stabilizes the system. Without it, high Z-Power would lead to infinite dissipation (burnout). With it, the system 'locks' into a stable resonance.")
