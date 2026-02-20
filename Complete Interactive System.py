import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time, math
from ipywidgets import FloatSlider, Button, HTML, VBox, HBox, Layout, Output, Checkbox, BoundedFloatText
from IPython.display import display, clear_output

# ==========================================
# 1. CORE SIMULATION ENGINE (v2 - Pulse Map)
# ==========================================
def simulate_v2(T, dt, omega, mu0, ramp, beta, gamma, theta0, K0, alpha, Rc, b, c, R0, th0, X0, sigma, pulse_map):
    steps = int(T / dt)
    t_axis = np.linspace(0, T, steps)
    
    R = np.zeros(steps); th = np.zeros(steps); X = np.zeros(steps)
    R[0] = R0; th[0] = th0; X[0] = X0
    
    current_th = th0
    
    for i in range(1, steps):
        t = t_axis[i]
        
        # Check Pulse Map (Phase Shift)
        # Using a small epsilon to catch the pulse time
        for p_t, p_phi in pulse_map.items():
            if abs(t - p_t) < dt/2:
                current_th += p_phi
        
        # Dynamics
        mu = mu0 + ramp * t
        Z = np.sqrt(np.abs(np.exp(1j * current_th) + 1)**2) # Dissonance
        
        # Phase Dynamics (Kuramoto-like)
        dth = (omega - gamma * R[i-1]**2 - K0 * R[i-1] * np.sin(current_th - theta0)) * dt
        noise = sigma * np.sqrt(dt) * np.random.randn()
        current_th += dth + noise
        
        # Resource Dynamics
        dR = (mu * R[i-1] - beta * R[i-1]**3 - 0.2 * Z**2) * dt
        R[i] = max(0.01, R[i-1] + dR)
        
        # Phase Transition (Order Parameter X)
        a_R = alpha * (Rc - R[i])
        dX = (- (a_R * X[i-1] + b * X[i-1]**3)) * dt
        X[i] = X[i-1] + dX
        
        th[i] = current_th
        
    return t_axis, R, th, X

# ==========================================
# 2. UI COMPONENTS & LOGIC
# ==========================================

# Data storage
pulse_map = {}
try:
    _mirror_log
except NameError:
    _mirror_log = pd.DataFrame(columns=['ts','Rhat','what','Zhat','dRhat','Z_before','Z_after','dZ'])

# Output areas
out = Output()
stat_panel = HTML("<b>Status:</b> Ready")

# Sliders - Simulation
T_slider = FloatSlider(description='Time (T)', value=100.0, min=10.0, max=500.0)
omega_slider = FloatSlider(description='ω (Noise)', value=0.5, min=0.0, max=2.0)
Rc_slider = FloatSlider(description='R_c (Limit)', value=0.15, min=0.05, max=0.3)
sigma_slider = FloatSlider(description='σ (Fluct)', value=0.05, min=0.0, max=0.2)

# Sliders - Subjective
Rhat = FloatSlider(description='R̂ Resources', value=3.0, min=1.0, max=5.0, step=0.5)
what = FloatSlider(description='ω̂ Disturbance', value=2.0, min=1.0, max=5.0, step=0.5)
Zhat = FloatSlider(description='Ẑ Dissonance', value=2.0, min=1.0, max=5.0, step=0.5)

# Pulse Control
tp_slider = FloatSlider(description='t_pulse', value=50.0, min=0.0, max=500.0)
btn_pi2 = Button(description='π/2 (90°)', button_style='warning', layout=Layout(width='100px'))
btn_pi = Button(description='π (180°)', button_style='danger', layout=Layout(width='100px'))
btn_clear_p = Button(description='Clear Pulse', layout=Layout(width='100px'))

# Logger
Z_before = FloatSlider(description='Ẑ Before', value=3.0, min=1.0, max=5.0, step=0.5)
Z_after = FloatSlider(description='Ẑ After', value=2.0, min=1.0, max=5.0, step=0.5)
btn_log = Button(description='Save Log', button_style='info')

# Main Run Button
btn_run = Button(description='Run Simulation ▶', button_style='success', layout=Layout(width='200px', height='40px'))

def update_pulse_list():
    if not pulse_map:
        return "No pulses registered."
    s = "<b>Registered Pulses:</b><br>"
    for t in sorted(pulse_map.keys()):
        s += f"t={t:.1f}: φ={pulse_map[t]/np.pi:.2f}π<br>"
    return s

pulse_display = HTML(update_pulse_list())

# --- Callbacks ---
def on_pi2_clicked(_):
    pulse_map[tp_slider.value] = np.pi/2
    pulse_display.value = update_pulse_list()

def on_pi_clicked(_):
    pulse_map[tp_slider.value] = np.pi
    pulse_display.value = update_pulse_list()

def on_clear_p_clicked(_):
    pulse_map.clear()
    pulse_display.value = update_pulse_list()

btn_pi2.on_click(on_pi2_clicked)
btn_pi.on_click(on_pi_clicked)
btn_clear_p.on_click(on_clear_p_clicked)

def on_run_clicked(_):
    # Mapping subjective to R0, omega
    R0_mapped = 0.05 + 0.03 * (Rhat.value - 1)
    omega_mapped = 0.1 + 0.2 * (what.value - 1)
    
    with out:
        clear_output(wait=True)
        t, R, th, X = simulate_v2(
            T=T_slider.value, dt=0.1, omega=omega_mapped, mu0=0.02, ramp=0.0001,
            beta=0.5, gamma=0.1, theta0=np.pi, K0=0.05, alpha=1.0, Rc=Rc_slider.value,
            b=1.0, c=1.0, R0=R0_mapped, th0=0.0, X0=0.0, sigma=sigma_slider.value,
            pulse_map=pulse_map
        )
        
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Resource & Transition
        ax1 = fig.add_subplot(221)
        ax1.plot(t, R, color='green', label='Resource R')
        ax1.axhline(Rc_slider.value, color='red', linestyle='--', label='Threshold Rc')
        ax1.set_title("Resource Dynamics & Criticality")
        ax1.legend()
        
        # 2. Phase Dynamics
        ax2 = fig.add_subplot(222)
        ax2.plot(t, np.sin(th), color='blue', alpha=0.6, label='sin(θ) [Love-Darkness]')
        for pt in pulse_map.keys():
            ax2.axvline(pt, color='orange', linestyle=':', label='Pulse' if pt==list(pulse_map.keys())[0] else "")
        ax2.set_title("Phase Dynamics (Love ↔ Darkness)")
        ax2.set_ylabel("+1: Love / -1: Darkness")
        ax2.legend()

        # 3. 3D Trajectory (Soul State)
        ax3 = fig.add_subplot(212, projection='3d')
        # We plot X (Real), sin(th) (Imag), and Time or R
        real_comp = R * np.cos(th)
        imag_comp = R * np.sin(th)
        ax3.plot(real_comp, imag_comp, t, label='Soul Path', color='purple')
        ax3.set_xlabel('Ego / Real (x)')
        ax3.set_ylabel('Love / Imag (y)')
        ax3.set_zlabel('Time (Evolution)')
        ax3.set_title("3D Soul State Trajectory (Z-Axis represents Evolution)")
        
        plt.tight_layout()
        plt.show()

btn_run.on_click(on_run_clicked)

# --- Layout ---
box_sub = VBox([HTML("<h3>1. Subjective Meter</h3>"), Rhat, what, Zhat, btn_run])
box_sim = VBox([HTML("<h3>2. Simulation Tuning</h3>"), T_slider, omega_slider, Rc_slider, sigma_slider])
box_pulse = VBox([HTML("<h3>3. Phase Pulse Control</h3>"), tp_slider, HBox([btn_pi2, btn_pi, btn_clear_p]), pulse_display])
box_log = VBox([HTML("<h3>4. MIRROR-3D Logger</h3>"), HBox([Z_before, Z_after]), btn_log])

ui = VBox([
    HTML("<h1 style='text-align:center;'>Inversion of Love and Darkness: LoveOS v2.0</h1>"),
    HBox([box_sub, box_sim], layout=Layout(justify_content='space-around')),
    HBox([box_pulse, box_log], layout=Layout(justify_content='space-around')),
    out
])

display(ui)
