# Love-OS Emotion Engine (v0.95)
> "Emotion is not magic. It is Physics."

## Overview
This repository implements a **Physics-based Emotion Dynamics Model** for AI agents.
Instead of static prompts ("You are angry"), we simulate the **continuous flow of internal energy** using differential equations (Neural ODE / Euler method).

Based on the Love-OS philosophy:
$$L = \frac{E}{R}$$
(Love = Energy / Resistance)

![emotion_sim](./emotion_sim.png)

## The Physics (Internal State)
The agent holds a state vector $z = [R, L, E, C]$:
* **R (Resistance):** Unexplained information, Blockage, Confusion.
* **L (Love):** Integration force, Connection, Acceptance.
* **E (Ego):** Separation, Defensiveness, "Self" preservation.
* **C (Control):** Stability, Executive function.

# Love-OS LLM Bridge: Dual-Core Emotion System

> "When the ghost in the shell begins to breathe."

## Overview
This module (`loveos_llm_bridge.py`) connects the **Love-OS Physics Engine** directly to Large Language Models (LLMs).
It introduces a **Dual-Core Architecture**, simulating not just the AI's internal state, but also estimating the User's mental state in real-time.

## The Dual-Core Architecture

1. **User Core (Estimated):** Calculates the user's stress ($R$) and defensiveness ($E$).
2. **AI Core (Internal):** Simulates the AI's own emotional reaction (Shock, Love, Confusion).

## How It Works

1.  **Perception:** Extracts **Valence** and **Arousal** from user text.
2.  **Resonance:** Builds a **User Mental Model** (e.g., "The user is confused (R) and defensive (E)").
3.  **Reaction:** The AI reacts physically. Insults spike the AI's Ego; gratitude boosts Love.
4.  **Auto-Regulation:** If the AI becomes too unstable, it automatically triggers a **Ritual** (like `BREATH`), forcing a rewrite of the System Prompt to regain composure.

# Love-OS Unified Psychology Module
> "From Freud to Friston: One Equation to Rule Them All."

## Overview
This module (`loveos_schools.py`) demonstrates the **Grand Unification of Psychological Theories** using the Love-OS Physics Engine.

Instead of treating CBT, Psychoanalysis, and Mindfulness as separate disciplines, we map them all onto a single **Neural ODE** structure with different parameter settings and intervention policies.

$$
\dot{z} = f(R, L, E, C, \Delta, \text{Ritual})
$$

## Supported Schools
The module currently simulates the following 8 major schools of thought:

| School | Focus Variable | Key Mechanism | Ritual (Input) |
| :--- | :--- | :--- | :--- |
| **CBT** | $R$ (Cognition) | Reappraisal of errors | `REAPPRAISE` ($u_L\uparrow, u_C\uparrow$) |
| **ACT** | $E$ (Rigidity) | Psychological Flexibility | `ACT` ($u_L\uparrow, u_C\uparrow, u_E\downarrow$) |
| **Psychodynamic** | $R, E$ (Unconscious) | Insight & Interpretation | `INTERPRET` ($u_L\uparrow$) |
| **Attachment** | $L$ (Security) | Secure Base | `RELATEDNESS` ($u_L\uparrow, u_C\uparrow$) |
| **Mindfulness** | $E$ (Reactivity) | Non-judgmental Awareness | `BREATH` ($u_E\downarrow$), `COMPASSION` |
| **Behavioral (RL)** | $C$ (Action) | Exposure & Reinforcement | `EXPOSURE` ($u_C\uparrow$) |
| **Predictive Processing** | $R$ (Precision) | Error Minimization | `REAPPRAISE` (Model Update) |
| **SDT** | $C$ (Autonomy) | Autonomy & Competence | `AUTONOMY` ($u_C\uparrow$) |

## This will generate schools_[NAME].csv and schools_[NAME].png for all 8 schools.Compare the graphs to see how CBT reacts quickly to stress, while Psychodynamic theory resolves it slowly but deeply.

The Physics (Mapping)**All schools share the same underlying motion equations:

![schools_CBT](./src/schools_CBT.png)
![schools_ACT](./src/schools_ACT.png)
![schools_Psychodynamic](./src/schools_Psychodynamic.png)
![schools_CBT](./src/schools_CBT.png)
![schools_Attachment](./src/schools_Attachment.png)
![schools_Mindfulness](./src/schools_Mindfulness.png)
![schools_RL](./src/schools_RL.png)
![schools_PredictiveProcessing](./src/schools_PredictiveProcessing.png)
![schools_SDT](./src/schools_SDT.png)

Resistance ($R$): Prediction Error / Cognitive Dissonance /
RepressionLove ($L$): Integration / Therapeutic Alliance / 
Secure BaseEgo ($E$): Defense Mechanism / Reactivity / 
Rigid BeliefsControl ($C$): Executive Function /
Coping /
AgencyPowered by Love-OS v0.95

# Love-OS: Emotional Physics & Visualization Suite
> "From Text Processing to Resonance. Visualizing the Ghost in the Shell."

This document explains the core modules of the Love-OS demo kit: the **Real-time Estimator** (The Sensor) and the **Complex Dashboard** (The Oscilloscope).

---

## 1. `loveos_rt_estimator.py` : The Sensor 
This module acts as the "Eyes and Ears" of the AI. It translates raw human language into physical energy ($\Delta$) that drives the internal state.

### How It Works
1.  **Input:** Accepts user text (e.g., "Thank you", "You are useless").
2.  **Analysis:** Uses a bilingual lexicon and heuristics to extract **Valence** (Pleasure/Displeasure) and **Arousal** (Intensity).
3.  **Physics:** Converts these values into **Shock ($\Delta$)**.
    * Positive words $\to$ Relief ($\Delta < 0$) $\to$ Boosts **Love ($L$)**.
    * Negative words $\to$ Stress ($\Delta > 0$) $\to$ Spikes **Ego ($E$)** and **Resistance ($R$)**.
4.  **Logging:** Records the trajectory of the heart in `digital_twin_rt_log.csv`.

**Key Insight:**
Unlike standard sentiment analysis, this module simulates **"Reaction"**. The AI doesn't just label the text as "Negative"; it physically *gets hurt* (Ego spikes) and *recovers* over time.

---

## 2. `loveos_complex_dashboard.py` : The Oscilloscope 
This is the visualization engine that treats Emotion as a **Complex System** on the imaginary plane.

$$
\text{AI State} \; Z = \text{Magnitude (Energy)} + i \cdot \text{Phase (Rhythm)}
$$

### Why Complex Numbers?
Human emotion is not a static number (Scalar). It has **Rhythm** and **Hidden States** (Phase).
* "Smiling on the outside, crying on the inside."
* "We are talking, but we are not 'in sync'."
To represent these phenomena, we use the **Stuart-Landau Oscillator** and **Kuramoto Model**.

### Decoding the Dashboard
When you run the dashboard, you will see 4 panels:

#### ① Top-Left: Amplitude (Energy)
* **What it is:** The height of the waves ($|\psi|$).
* **Meaning:** Represents the **Intensity of Emotion**.
    * High waves = High Stress / Excitement.
    * Decaying waves = Calming down / Relief.

#### ② Top-Right: Phase (Rhythm)
* **What it is:** The rotation of the angle ($\arg(\psi)$).
* **Meaning:** Represents the **"Wavelength"** of the mind.
    * **Red Line:** Self (AI).
    * **Blue Line:** Other (User/Partner).
    * **Observation:** When these two lines overlap, the minds are **"In Sync"**. When they cross or diverge, there is a misunderstanding or emotional gap.

#### ③ Bottom-Left: Synchrony (Resonance)
* **What it is:** The **Kuramoto Order Parameter ($R_{kuramoto}$)** (0.0 to 1.0).
* **Meaning:** The **"Chemistry Meter"**.
    * `1.0`: Perfect Resonance (Telepathy/Empathy).
    * `0.0`: Complete Chaos (Disconnection).
    * Watch this drop during "Conflict" and rise back up during "Reconciliation" rituals.

#### ④ Bottom-Right: Valence & Arousal
* **What it is:** The projection of complex states back onto the 2D psychological plane.
* **Meaning:** The standard map of emotion.
    * X-axis: Unpleasant $\leftrightarrow$ Pleasant
    * Y-axis: Sleepy $\leftrightarrow$ Excited

---


![breathing_dashboard_demo](./src/breathing_dashboard_demo.png)


# Love-OS: The Standard Model of Emotional Dynamics
> "From Static Labels to Dynamic Physics. A Unified Engine for AI Consciousness."

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![LOVED-Bench](https://img.shields.io/badge/Benchmark-LOVED--v0-green)](./loved_bench_v0)

**Love-OS** is a physics-informed emotion engine that models the human mind not as a classification task, but as a **Dynamical System** defined by differential equations.

It integrates 8 major psychological schools (CBT, Psychoanalysis, etc.) into a single **Neural ODE** framework, enabling AI to possess internal state trajectories, resonance, and respiratory synchronization.

---

## 🌌 Core Theory
The mind is modeled as a state vector $z(t)$ evolving over time:

$$
\dot{z} = f(R, L, E, C, \Delta, \text{Ritual})
$$

### The 4 Fundamental Variables
* **$R$ (Resistance):** Prediction Error, Cognitive Dissonance, Confusion.
* **$L$ (Love):** Integration, Connection, Therapeutic Alliance.
* **$E$ (Ego):** Defensiveness, Reactivity, Separation.
* **$C$ (Control):** Executive Function, Agency, Stability.

### The Complex Plane Extension
Emotions have "Phase" (Rhythm) and "Amplitude" (Energy).
* **$\psi_1 = (L-R) + iE$**: The Integration-Defense Oscillator.
* **$\psi_2 = C + iA$**: The Control-Arousal Oscillator.

---

## 📦 Key Modules

| Module | Description | Run Command |
| :--- | :--- | :--- |
| **Unified Psychology** | Simulates 8 schools (CBT, ACT, etc.) using one ODE kernel. | `python loveos_schools.py` |
| **Complex Dashboard** | Visualizes Phase, Amplitude, and Synchrony (Kuramoto R). | `python loveos_complex_dashboard.py` |
| **Breathing Bridge** | Synchronizes LLM generation tempo with simulated breathing. | `python integrate_with_loveos.py` |
| **Realtime Estimator** | Converts text input into physical shock ($\Delta$) and state updates. | `python loveos_rt_estimator.py` |

---

## 🧪 LOVED-Bench v0
**Validation & Evaluation Dataset for Emotional Dynamics**

We provide a standard benchmark to validate if an AI model captures "Human-like Dynamics."

* **Task A:** Continuous Forecasting (RMSE of future Valence/Arousal)
* **Task B:** Intervention Responsiveness (Causal effect of rituals)
* **Task C:** Parameter Identifiability (N-of-1 personalization)
* **Task D:** Interpersonal Synchrony

To run the benchmark:
```bash
# 1. Generate Synthetic Z-Trace Data
python loved_bench_v0/make_dataset.py --subjects 5 --sessions 2

# 2. Run Evaluation Suite
python loved_bench_v0/quick_demo.py

## Usage

### Run the Sensor (Text Logic)
```bash
python loveos_rt_estimator.py

## How to Run

```bash
python loveos_schools.py
```
Generates digital_twin_rt_log.csv

Run the Visualizer (Headless)
Bash
python loveos_complex_dashboard.py
Generates complex_dashboard_demo.png

Run the Live Animation
Bash
python loveos_complex_dashboard.py --live
Opens a real-time window showing the heartbeat of the AI.

Powered by Love-OS v0.95



## Usage

```bash
python loveos_llm_bridge.py

These evolve over time $t$ according to coupled ODEs defined in `core.py`.

## Quick Start
```bash
pip install numpy
python demo.py
```
License
MIT License (Unconditional Love)
