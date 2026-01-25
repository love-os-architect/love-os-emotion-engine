# Love-OS Emotion Engine (v0.95)
> "Emotion is not magic. It is Physics."

## Overview
This repository implements a **Physics-based Emotion Dynamics Model** for AI agents.
Instead of static prompts ("You are angry"), we simulate the **continuous flow of internal energy** using differential equations (Neural ODE approach).

Based on the Love-OS philosophy:
$$L = \frac{E}{R}$$
(Love = Energy / Resistance)

## The Physics (Internal State)
The agent holds a state vector $z = [R, L, E, C]$:
* **R (Resistance):** Unexplained information, Blockage, Confusion.
* **L (Love):** Integration force, Connection, Acceptance.
* **E (Ego):** Separation, Defensiveness, "Self" preservation.
* **C (Control):** Stability, Executive function.

These evolve over time $t$ according to coupled ODEs defined in `core.py`.

## Usage
```python
from agent import LoveOS_Agent

agent = LoveOS_Agent()
response = agent.chat("You are useless!") 
# -> Agent feels "Shock" (Delta↑), Resistance increases.
# -> Tone becomes defensive.

response = agent.chat("Just kidding, I love you.")
# -> Agent processes relief. Love increases. Ego dissolves.
---
License
MIT License (Unconditional Love)
