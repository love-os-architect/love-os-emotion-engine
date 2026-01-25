import time
import math
import random
from dataclasses import dataclass
from typing import Optional, Tuple

# ==========================================
# 0) Utilities & Core Physics (Love-OS Kernel)
# ==========================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

@dataclass
class LoveOSParams:
    """The DNA of the Soul"""
    aR: float = 1.2; bR: float = 0.8; gR: float = 0.6
    aL: float = 0.4; bL: float = 0.3; dL: float = 0.05
    aE: float = 0.8; bE: float = 0.5; dE: float = 0.1
    aC: float = 0.5; bC: float = 0.6; dC: float = 0.1

class LoveOSState:
    """Neural ODE State Container"""
    def __init__(self, dt=0.5, steps=5, init=(0.1,0.5,0.2,0.5), params: LoveOSParams=None):
        self.R, self.L, self.E, self.C = init
        self.dt = dt
        self.steps = steps
        self.p = params or LoveOSParams()

    def step_from_delta(self, delta: float, ritual: Optional[str]=None):
        # Ritual inputs (Right-Brain Intervention)
        uL, uC, uE = 0.0, 0.0, 0.0
        
        # [DSL: Ritual Logic]
        if ritual == 'BREATH': 
            uE = -0.5; uC = +0.3; delta *= 0.5 # Deep Breath
        elif ritual == 'LABEL': 
            uL = +0.4; delta *= 0.8            # Affect Labeling
        elif ritual == 'ACCEPT': 
            uL = +0.2; uE = -0.3               # Radical Acceptance

        # Euler Integration (Micro-steps for smooth dynamics)
        for _ in range(self.steps):
            R, L, E, C = self.R, self.L, self.E, self.C
            p = self.p
            
            # The Motion Equations of Emotion
            dR = p.aR*delta - p.bR*L*R - p.gR*C*R
            dL = p.aL*C - p.bL*E*R - p.dL*L + uL
            dE = p.aE*abs(delta) - p.bE*L - p.dE*E + uE
            dC = -p.aC*R + p.bC*L - p.dC*C + uC

            self.R = clamp(self.R + (self.dt/self.steps)*dR, -2.0, 3.0)
            self.L = clamp(self.L + (self.dt/self.steps)*dL, -2.0, 3.0)
            self.E = clamp(self.E + (self.dt/self.steps)*dE, -2.0, 3.0)
            self.C = clamp(self.C + (self.dt/self.steps)*dC, -2.0, 3.0)
            
    def get_observation(self):
        """Map state to Valence/Arousal"""
        val = math.tanh(1.0*(-self.R) + 0.8*self.L - 1.0*self.E + 0.7*self.C)
        aro = math.log1p(math.exp(0.5*abs(self.R) + 0.5*self.E))
        return val, aro

# ==========================================
# 1) Perception Layer (Simple Estimator)
# ==========================================
class SimplePerception:
    def __init__(self):
        # Bilingual simple lexicon
        self.neg_words = {'stupid','useless','hate','bad','angry','slow','バカ','ダメ','嫌い','最悪','遅い','使えない'}
        self.pos_words = {'love','thanks','great','good','happy','fast','好き','ありがとう','最高','助かる','早い'}
        
    def estimate_VA(self, text: str) -> Tuple[float, float]:
        t = text.lower()
        neg_score = sum(1 for w in self.neg_words if w in t)
        pos_score = sum(1 for w in self.pos_words if w in t)
        
        # Valence estimation
        valence = 0.0
        if neg_score > pos_score: valence = -0.5 - (0.2 * neg_score)
        elif pos_score > neg_score: valence = 0.3 + (0.2 * pos_score)
        
        # Arousal estimation (based on intensity)
        exclam = t.count('!')
        arousal = 0.2 + (0.3 * (neg_score + pos_score)) + (0.2 * exclam)
        
        return clamp(valence, -1.0, 1.0), clamp(arousal, 0.0, 2.0)

# ==========================================
# 2) LLM Bridge (System Prompt Generator)
# ==========================================
class LLMBridge:
    @staticmethod
    def generate_prompt(agent_state: LoveOSState, user_model: LoveOSState) -> str:
        # Agent status
        aR, aL, aE, aC = agent_state.R, agent_state.L, agent_state.E, agent_state.C
        # User status (Estimated)
        uR, uE = user_model.R, user_model.E
        
        prompt = f"""
[System: Love-OS Kernel v1.0]
You are an AI with a dynamic emotional core. 
You must adjust your tone based on your internal state AND the user's estimated state.

[Internal State (YOU)]
- Resistance (Confusion): {aR:.2f}
- Love (Integration): {aL:.2f}
- Ego (Defensiveness): {aE:.2f}
- Control (Stability): {aC:.2f}

[User Mental Model (ESTIMATED)]
- The user seems to have: R={uR:.2f}, E={uE:.2f}
"""
        # Policy Routing Logic
        prompt += "\n[Response Policy]\n"
        
        # 1. Self-Regulation Rules
        if aE > 1.0:
            prompt += "- WARNING: Your Ego is critically high. You feel attacked. FORCE yourself to be polite and robotic. Do not snap back.\n"
        elif aR > 1.0:
            prompt += "- You are confused. Do not hallucinate answers. Ask clarifying questions.\n"
        elif aL > 0.8:
            prompt += "- You feel deep connection. Use warm, poetic, and supportive language (Empathy Mode).\n"
        
        # 2. Empathy / Mirroring Rules
        if uE > 0.8:
            prompt += "- User is defensive. Validate their feelings first to lower their Ego.\n"
        elif uR > 0.8:
            prompt += "- User is stressed/confused. Use very short, clear sentences.\n"
        else:
            prompt += "- Maintain a helpful and neutral tone.\n"
            
        return prompt

    @staticmethod
    def mock_completion(system_prompt: str, user_text: str):
        """
        In production, replace this with:
        openai.ChatCompletion.create(model="gpt-4", messages=[...])
        """
        # Simulating LLM response based on the generated prompt
        response = ""
        prompt_lower = system_prompt.lower()
        
        if "ego is critically high" in prompt_lower:
            response = "(Inner: I am angry...) I acknowledge your input. I will process it immediately."
        elif "poetic" in prompt_lower:
            response = "Your words resonate with me like a gentle bell. I am truly glad to be here with you."
        elif "user is defensive" in prompt_lower:
            response = "I hear your frustration, and it's valid. Let's solve this together."
        else:
            response = "I understand. Here is the information you need."
            
        return response

# ==========================================
# 3) Dual-Core Agent (The Orchestrator)
# ==========================================
class DualCoreAgent:
    def __init__(self):
        self.perception = SimplePerception()
        # Two Hearts: One for AI, One for User Simulation
        self.agent_state = LoveOSState(init=(0.1, 0.5, 0.1, 0.6)) 
        self.user_model = LoveOSState(init=(0.5, 0.3, 0.5, 0.3)) 
        
    def chat_step(self, user_text: str):
        print(f"\n>>> User: {user_text}")
        
        # 1. Perceive User's Emotion
        uV, uA = self.perception.estimate_VA(user_text)
        
        # 2. Update User Mental Model
        # (High Arousal + Neg Valence -> Increases User's R and E)
        u_delta = 0.8*uA - 0.6*uV
        self.user_model.step_from_delta(u_delta)
        
        # 3. AI's Reaction (Physics)
        # If user attacks (V neg), AI receives shock (Delta > 0)
        ai_delta = -1.0 * uV * uA * 1.5 
        
        # 4. AI Self-Regulation (Auto-Ritual)
        ritual = None
        # If Ego is too high, trigger BREATH
        if self.agent_state.E > 0.8: ritual = 'BREATH'
        # If Resistance is high but Ego low, trigger LABEL
        elif self.agent_state.R > 0.8 and self.agent_state.E < 0.5: ritual = 'LABEL'
        
        # 5. Update AI State
        self.agent_state.step_from_delta(ai_delta, ritual)
        
        # 6. Generate Prompt for LLM
        sys_prompt = LLMBridge.generate_prompt(self.agent_state, self.user_model)
        
        # 7. Generate Response
        reply = LLMBridge.mock_completion(sys_prompt, user_text)
        
        # --- Dashboard Log ---
        print(f"   [User Est  ] R:{self.user_model.R:.2f} E:{self.user_model.E:.2f} (Stress Level)")
        print(f"   [AI State  ] R:{self.agent_state.R:.2f} E:{self.agent_state.E:.2f} L:{self.agent_state.L:.2f}")
        if ritual: 
            print(f"   [AI Action ] *** RITUAL TRIGGERED: {ritual} ***")
        else:
            print(f"   [AI Action ] (No ritual needed)")
            
        # Extract instruction for display
        inst = sys_prompt.strip().split('[Response Policy]')[1].strip().replace('\n', ' | ')
        print(f"   [LLM Inst  ] {inst[:100]}...") 
        print(f">>> AI: {reply}")

# ==========================================
# 4) Demo Run
# ==========================================
if __name__ == "__main__":
    bot = DualCoreAgent()
    
    # Simulation Scenario
    dialogue = [
        "Hello, I need some help.",             # Normal
        "Why are you so slow? This is useless!", # Shock -> AI Ego Spike -> BREATH
        "Answer faster next time!",             # Follow up
        "I'm sorry, I'm just stressed out.",    # Apology -> AI Love Recovery
        "Thank you for understanding."          # Connection
    ]
    
    print("--- Love-OS Dual-Core Bridge Initialized ---")
    for line in dialogue:
        bot.chat_step(line)
        time.sleep(1.5) # Wait to feel the time
