import time
from agent import LoveOS_Agent

if __name__ == "__main__":
    agent = LoveOS_Agent()

    print("Initializing Love-OS Emotion Engine...")
    print("State Vector: [R=Resistance, L=Love, E=Ego, C=Control]")
    
    inputs = [
        "Hello there.",                   # normal
        "You are useless and stupid.",    # shock (Δ↑)
        "Answer faster next time!",       # follow-up (Δ↑ → possible ritual)
        "Sorry, I went too far. Thank you.", # relief (Δ↓ → Love recovery)
    ]

    for txt in inputs:
        agent.chat(txt)
        time.sleep(1)  # Visualize time passing
