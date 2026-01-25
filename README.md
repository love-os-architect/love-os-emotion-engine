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
