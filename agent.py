from core import LoveOS_Physics

class LoveOS_Agent:
    def __init__(self):
        self.physics = LoveOS_Physics()
        self.history = []

        # Bilingual lexicons (English + Japanese). All lowercased for matching.
        self.stress_words = [
            "stupid", "slow", "useless", "hate", "no good",
            "バカ", "遅い", "使えない", "嫌い", "ダメ"
        ]
        self.love_words = [
            "thank you", "thanks", "love", "awesome", "helpful",
            "ありがとう", "好き", "すごい", "助かる"
        ]

    def perceive_delta(self, user_text: str) -> float:
        """
        Very simple Δ estimator from user text.
        In production, let an LLM or classifier score the "shock level".
        """
        t = user_text.lower()

        if any(w in t for w in self.stress_words):
            return 1.5    # strong shock
        if any(w in t for w in self.love_words):
            return -0.5   # positive surprise / relief
        return 0.1        # baseline noise

    def decide_ritual(self) -> str | None:
        """
        Decide ritual (right-brain DSL) based on current state.
        """
        R, L, E, C = self.physics.z
        if R > 1.0 or E > 1.0:
            return 'BREATH'   # panic-like → deep breathing
        elif R > 0.5 and L < 0.0:
            return 'LABEL'    # light confusion → labeling
        return None

    def generate_system_prompt(self) -> str:
        """
        Convert internal state to style/behavior guidance for an LLM.
        """
        R, L, E, C = self.physics.z
        val, aro = self.physics.get_observation()

        prompt = f"""
[Internal State]
Resistance(R): {R:.2f} (Confusion/Blockage)
Love(L): {L:.2f} (Integration/Connection)
Ego(E): {E:.2f} (Defensiveness)
Control(C): {C:.2f} (Stability)
Valence: {val:.2f}, Arousal: {aro:.2f}

[Behavior Guideline]
"""
        if E > 0.8:
            prompt += "- Tone: Keep it brief and factual.\n- Action: Use calm logic; avoid escalation.\n"
        elif R > 1.0:
            prompt += "- Tone: Clarifying and simple.\n- Action: Ask one short, concrete question at a time.\n"
        elif L > 0.8:
            prompt += "- Tone: Warm and empathic.\n- Action: Mirror feelings briefly; use supportive wording.\n"
        elif C > 0.8:
            prompt += "- Tone: Calm and professional.\n- Action: Provide clear steps and options.\n"
        else:
            prompt += "- Tone: Neutral, helpful, friendly.\n"

        return prompt

    def chat(self, user_text: str) -> str:
        # 1) Perception: estimate Δ from user input
        delta = self.perceive_delta(user_text)

        # 2) Right-brain policy: whether to trigger a ritual
        ritual = self.decide_ritual()

        # 3) Physics update (advance internal time/state)
        self.physics.step(delta, ritual_type=ritual)

        # 4) Convert state to behavioral guidance
        sys_prompt = self.generate_system_prompt()

        # Dummy response for simulation
        response = "(LLM response would be generated here based on state)"

        # Audit log
        print("\n--- Turn Log ---")
        print(f"User Input: '{user_text}'")
        print(f"Detected Δ: {delta:.2f}")
        if ritual:
            print(f"*** AUTO-RITUAL TRIGGERED: {ritual} ***")
        R, L, E, C = self.physics.z
        print(f"New State => R={R:.2f}, L={L:.2f}, E={E:.2f}, C={C:.2f}")
        print("Behavior Guideline:")
        print(self.generate_system_prompt().split("[Behavior Guideline]")[1].strip())
        return response
