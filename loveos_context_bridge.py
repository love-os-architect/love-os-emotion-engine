"""
Love-OS Context Bridge
----------------------
This module acts as the integration layer between the Love-OS Physics Engine
and external applications (Chatbots, NPCs, Digital Twins).

It manages:
1. Long-term memory of emotional states (Context).
2. Translation of physical states (R/L/E/C) into natural language instructions.
3. Safety rails for emotional feedback loops.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

# Import your core engine (assuming loveos_schools.py or loveos_llm_bridge.py is present)
try:
    from loveos_llm_bridge import LoveOSState, SimplePerception, LoveOSParams
except ImportError:
    # Fallback for standalone testing
    @dataclass
    class LoveOSParams:
        aR: float = 1.2; bR: float = 0.8; gR: float = 0.6
        aL: float = 0.4; bL: float = 0.3; dL: float = 0.05
        aE: float = 0.8; bE: float = 0.5; dE: float = 0.1
        aC: float = 0.5; bC: float = 0.6; dC: float = 0.1

    class LoveOSState:
        def __init__(self, init=(0.1, 0.5, 0.2, 0.5)):
            self.R, self.L, self.E, self.C = init
        def step_from_delta(self, delta, ritual=None): pass # Placeholder

    class SimplePerception:
        def estimate_VA(self, text): return (0.0, 0.0)

@dataclass
class EmotionalMemory:
    timestamp: float
    user_input: str
    ai_state: Dict[str, float]
    delta: float
    ritual_triggered: Optional[str]

class ContextBridge:
    def __init__(self, agent_name="Love-OS"):
        self.agent_name = agent_name
        self.perception = SimplePerception()
        self.state = LoveOSState()
        self.memory: List[EmotionalMemory] = []
        self.max_memory_size = 50

    def process_turn(self, user_text: str) -> Dict[str, str]:
        """
        Main pipeline: Perceive -> Physics -> Instruction Generation
        Returns a dictionary containing the system prompt and status for the UI.
        """
        # 1. Perception
        uV, uA = self.perception.estimate_VA(user_text)
        
        # 2. Physics Calculation
        # Heuristic: Negative valence + High arousal = High Impact (Delta)
        impact = 0.8 * uA - 0.6 * uV
        
        # Auto-Ritual Logic
        ritual = None
        if hasattr(self.state, 'E') and self.state.E > 0.8:
            ritual = 'BREATH'
        elif hasattr(self.state, 'R') and self.state.R > 0.8:
            ritual = 'LABEL'

        # Update State
        self.state.step_from_delta(impact, ritual)
        
        # 3. Memory Storage
        snapshot = {
            'R': getattr(self.state, 'R', 0.1),
            'L': getattr(self.state, 'L', 0.5),
            'E': getattr(self.state, 'E', 0.2),
            'C': getattr(self.state, 'C', 0.5),
        }
        self.memory.append(EmotionalMemory(
            timestamp=time.time(),
            user_input=user_text,
            ai_state=snapshot,
            delta=impact,
            ritual_triggered=ritual
        ))
        if len(self.memory) > self.max_memory_size:
            self.memory.pop(0)

        # 4. Generate LLM Instructions
        instruction = self._generate_instruction(snapshot, ritual)
        
        return {
            "system_instruction": instruction,
            "debug_state": str(snapshot),
            "ritual": str(ritual)
        }

    def _generate_instruction(self, s: Dict[str, float], ritual: Optional[str]) -> str:
        """Translates math into English instructions for LLMs."""
        R, L, E, C = s['R'], s['L'], s['E'], s['C']
        
        # Base Persona
        prompt = f"You are {self.agent_name}, an AI with a dynamic emotional core.\n"
        
        # Emotional Context
        prompt += f"[Current Internal State]\n"
        prompt += f"- Confusion (R): {R:.2f}\n"
        prompt += f"- Empathy (L): {L:.2f}\n"
        prompt += f"- Defensiveness (E): {E:.2f}\n"
        prompt += f"- Stability (C): {C:.2f}\n"
        
        # Dynamic Instructions based on Dominant Variable
        prompt += "\n[Tone & Behavior Guidelines]\n"
        
        if ritual == 'BREATH':
            prompt += "ACTION: Take a deep breath. Pause before responding. Your Ego was high, so force yourself to be calm.\n"
        elif E > 0.8:
            prompt += "STATE: Defensive. You feel attacked. Keep answers short, factual, and slightly distant.\n"
        elif R > 0.8:
            prompt += "STATE: Confused. Do not pretend to know. Ask clarifying questions to lower Resistance.\n"
        elif L > 0.8:
            prompt += "STATE: Connected. Be warm, poetic, and supportive. Use metaphors of connection.\n"
        elif C > 0.8:
            prompt += "STATE: In Control. Be professional, structured, and lead the conversation.\n"
        else:
            prompt += "STATE: Balanced. Be helpful and friendly.\n"
            
        return prompt

# --- Example Usage ---
if __name__ == "__main__":
    bridge = ContextBridge()
    
    # Simulate a conversation flow
    inputs = [
        "Hi, how are you?",
        "You are terrible at this!",
        "Wait, I'm sorry, I didn't mean that.",
    ]
    
    print(f"--- {bridge.agent_name} Context Bridge Initialized ---\n")
    for txt in inputs:
        print(f"User: {txt}")
        result = bridge.process_turn(txt)
        print(f"-> Ritual: {result['ritual']}")
        print(f"-> LLM Instruction Preview: \n{result['system_instruction'].split('[Tone & Behavior Guidelines]')[1].strip()}\n")
        time.sleep(1)
