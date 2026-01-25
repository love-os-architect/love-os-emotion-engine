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

![schools_SDT](./src/schools_SDT.png)

## How to Run

```bash
python loveos_schools.py

## Usage

```bash
python loveos_llm_bridge.py

These evolve over time $t$ according to coupled ODEs defined in `core.py`.

## Quick Start
```bash
pip install numpy
python demo.py
---
License
MIT License (Unconditional Love)
