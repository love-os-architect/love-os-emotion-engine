import numpy as np
import matplotlib.pyplot as plt

def simulate_quantum_surrender(alpha_val=1.5, n_steps=100, n_trials=1000):
    """
    Simulates the difference between 'Fixed Ego' (Kennedy) 
    and 'Continuous Surrender' (Dolinar) in perceiving reality.
    """
    dt = 1.0 / n_steps
    eta = 1.0  # Ideal efficiency
    
    results = {'Kennedy': [], 'Dolinar': []}
    
    # Helstrom Bound (Theoretical Limit)
    helstrom_bound = 0.5 * (1 - np.sqrt(1 - np.exp(-4 * alpha_val**2)))

    for trial in range(n_trials):
        # Truth is either +alpha or -alpha
        true_hypothesis = np.random.choice([1, -1])
        alpha_true = true_hypothesis * alpha_val
        
        # --- 1. Kennedy Receiver (Fixed Displacement) ---
        # Strategy: Fix displacement to cancel +alpha, and never change.
        beta_ken = -alpha_val
        lambda_ken = eta * np.abs(alpha_true + beta_ken)**2
        clicks_ken = np.random.poisson(lambda_ken * 1.0)
        # Decision: If no clicks, assume +alpha. If clicks, assume -alpha.
        dec_ken = 1 if clicks_ken == 0 else -1
        results['Kennedy'].append(dec_ken == true_hypothesis)

        # --- 2. Dolinar Receiver (Sequential Surrender) ---
        # Strategy: Update belief and 'null' the most likely hypothesis at every step.
        p_plus = 0.5
        for _ in range(n_steps):
            # Surrender: Null the currently favored hypothesis
            beta_dol = -alpha_val if p_plus >= 0.5 else alpha_val
            
            # Physical interaction (Observation)
            lam = eta * np.abs(alpha_true + beta_dol)**2
            dn = np.random.poisson(lam * dt)
            
            # Bayesian Update (The 'Learning' process)
            # Probability of click given +alpha / -alpha
            l_plus = (eta * np.abs(alpha_val + beta_dol)**2 * dt)**dn * np.exp(-eta * np.abs(alpha_val + beta_dol)**2 * dt)
            l_minus = (eta * np.abs(-alpha_val + beta_dol)**2 * dt)**dn * np.exp(-eta * np.abs(-alpha_val + beta_dol)**2 * dt)
            
            p_plus = (p_plus * l_plus) / (p_plus * l_plus + (1 - p_plus) * l_minus)
            
        dec_dol = 1 if p_plus >= 0.5 else -1
        results['Dolinar'].append(dec_dol == true_hypothesis)

    # Calculate Error Rates
    err_ken = 1 - np.mean(results['Kennedy'])
    err_dol = 1 - np.mean(results['Dolinar'])

    print(f"--- Simulation Results (alpha={alpha_val}) ---")
    print(f"Kennedy (Fixed Ego) Error Rate: {err_ken:.4f}")
    print(f"Dolinar (Surrender) Error Rate: {err_dol:.4f}")
    print(f"Helstrom (Universal Limit)    : {helstrom_bound:.4f}")

if __name__ == "__main__":
    simulate_quantum_surrender()
