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

These evolve over time $t$ according to coupled ODEs defined in `core.py`.

## Quick Start
```bash
pip install numpy
python demo.py
---
License
MIT License (Unconditional Love)
