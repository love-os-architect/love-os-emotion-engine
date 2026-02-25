import math

class LoveOS_Node:

    def __init__(self, node_id, weight_lambda=0.5, R0=100.0, K0=10.0):

        self.node_id = node_id

        self.weight_lambda = weight_lambda # Balance between Body and Mind

        self.R0 = R0 # Base Resistance (Maximum friction of the Ego)

        self.K0 = K0 # Base Coupling Strength

        

        # State Variables

        self.c_body = 0.0

        self.c_mind = 0.0

        self.c_total = 0.0

        self.r_eff = R0

        self.k_eff = 0.0

    def _sigmoid_normalize(self, value, is_inverse=False):

        """Normalizes raw values to a 0.0 - 1.0 Conductivity Score."""

        # If is_inverse is True, a lower raw value means higher conductivity (e.g., Delay, EDA)

        norm = 1 / (1 + math.exp(-value))

        return 1.0 - norm if is_inverse else norm

    def update_state(self, hrv, eda, emg, resp_coh, alpha_beta, delay, speech_sync):

        """Updates Conductivity and Physical Parameters based on sensor data."""

        

        # 1. Calculate Body Conductivity (Geometric Mean)

        s_hrv = self._sigmoid_normalize(hrv)

        s_eda = self._sigmoid_normalize(eda, is_inverse=True)

        s_emg = self._sigmoid_normalize(emg, is_inverse=True)

        s_resp = self._sigmoid_normalize(resp_coh)

        self.c_body = (s_hrv * s_eda * s_emg * s_resp) ** 0.25

        # 2. Calculate Mind/Consciousness Conductivity (Geometric Mean)

        s_ab = self._sigmoid_normalize(alpha_beta)

        s_delay = self._sigmoid_normalize(delay, is_inverse=True)

        s_sync = self._sigmoid_normalize(speech_sync)

        self.c_mind = (s_ab * s_delay * s_sync) ** (1/3)

        # 3. Calculate Total Conductivity

        self.c_total = (self.c_body ** self.weight_lambda) * (self.c_mind ** (1 - self.weight_lambda))

        # 4. Map to Physical Parameters (The Core of Love-OS)

        # Higher conductivity means the Ego becomes thinner (lower resistance)

        self.r_eff = self.R0 * (1.0 - self.c_total) 

        # Higher conductivity amplifies the ability to connect/resonate

        self.k_eff = self.K0 * self.c_total         

    def handshake(self, other_node, zk_threshold=0.7):

        """P2P Handshake: Zero-Knowledge-like threshold verification."""

        print(f"\n--- Handshake Initiated: {self.node_id} & {other_node.node_id} ---")

        

        my_pass = self.c_total >= zk_threshold

        other_pass = other_node.c_total >= zk_threshold

        if my_pass and other_pass:

            print(f"[SUCCESS] Impedance matched. Initiating safe resonance protocol.")

            print(f"  {self.node_id} Resistance: {self.r_eff:.2f} | Coupling: {self.k_eff:.2f}")

            print(f"  {other_node.node_id} Resistance: {other_node.r_eff:.2f} | Coupling: {other_node.k_eff:.2f}")

            return True

        else:

            print(f"[REDAM/BLOCKED] High friction detected. Silence (/phase-shift) is recommended.")

            if not my_pass: print(f"  -> {self.node_id} Conductivity too low (Threshold: {zk_threshold})")

            if not other_pass: print(f"  -> {other_node.node_id} Conductivity too low (Threshold: {zk_threshold})")

            return False

# ===== Simulation Execution =====

# Node A (Awakened OS: Relaxed, thin ego, high perspective)

node_A = LoveOS_Node("Node_A(Awakened)")

node_A.update_state(hrv=2.0, eda=-2.0, emg=-2.0, resp_coh=2.0, alpha_beta=2.0, delay=-2.0, speech_sync=2.0)

# Node B (Ego OS: Tense, highly defensive, attached to X-axis)

node_B = LoveOS_Node("Node_B(Ego_Defensive)")

node_B.update_state(hrv=-1.0, eda=2.0, emg=1.5, resp_coh=-1.5, alpha_beta=-2.0, delay=1.5, speech_sync=-1.0)

# 1st Attempt: Fails due to Node B's high ego friction

node_A.handshake(node_B)

print("\n... Node_B executes deep breathing and self-observation (/phase-shift) ...")

# Node B updates state (Perspective rises, ego thins out)

node_B.update_state(hrv=1.5, eda=-1.0, emg=-1.5, resp_coh=1.8, alpha_beta=1.5, delay=-1.0, speech_sync=1.5)

# 2nd Attempt: Both egos are sufficiently thin. Handshake successful.

node_A.handshake(node_B)
