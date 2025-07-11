import numpy as np
import matplotlib.pyplot as plt

# --- Heston Model Simulation ---
def simulate_heston(kappa, theta, sigma=0.3, rho=-0.7, v0=0.04, S0=100, mu=0.0, T=1.0, N=252):
    dt = T / N
    S = np.zeros(N)
    v = np.zeros(N)
    S[0], v[0] = S0, v0

    for t in range(1, N):
        z1, z2 = np.random.normal(), np.random.normal()
        dW_v = np.sqrt(dt) * z1
        dW_S = rho * z1 * np.sqrt(dt) + np.sqrt(1 - rho**2) * z2 * np.sqrt(dt)

        # Update v with floor for numerical stability
        v_prev = max(v[t - 1], 1e-6)
        v[t] = max(v_prev + kappa * (theta - v_prev) * dt + sigma * np.sqrt(v_prev) * dW_v, 1e-6)
        S[t] = S[t - 1] + mu * S[t - 1] * dt + np.sqrt(v_prev) * S[t - 1] * dW_S

    return S, v

# --- Summary Statistics ---
def summary_stats(S, v):
    returns = np.diff(np.log(S))
    acf1 = np.corrcoef(returns[:-1], returns[1:])[0, 1] if len(returns) > 1 else 0
    return np.array([
        np.mean(returns),
        np.var(returns),
        np.mean(v),
        np.var(v),
        acf1
    ])

# --- Average over Multiple Simulations ---
def average_stats(kappa, theta, n_sim=5):
    stats = []
    for _ in range(n_sim):
        S_sim, v_sim = simulate_heston(kappa, theta)
        stats.append(summary_stats(S_sim, v_sim))
    return np.mean(stats, axis=0)

# --- Scaled Distance Function ---
def distance(s1, s2, scale=np.array([0.01, 0.01, 0.01, 0.01, 0.1])):
    return np.sqrt(np.sum(((s1 - s2) / scale) ** 2))

# --- ABC Rejection Algorithm ---
def abc_rejection(observed_stats, N=5000, epsilon=0.5, n_sim=20):
    accepted = []
    for _ in range(N):
        kappa = np.random.uniform(0.8, 1.5)
        theta = np.random.uniform(0.03, 0.07)
        sim_stats = average_stats(kappa, theta, n_sim=n_sim)
        d = distance(sim_stats, observed_stats)
        if d < epsilon:
            accepted.append((kappa, theta))
    return np.array(accepted)

# --- Step 1: Generate Observed Data ---
true_kappa = 1.2
true_theta = 0.05
S_obs, v_obs = simulate_heston(true_kappa, true_theta)
observed_stats = summary_stats(S_obs, v_obs)

# Diagnostic
true_stats = average_stats(true_kappa, true_theta, n_sim=20)
print("Observed summary stats:", observed_stats)
print("Simulated (true params) summary stats:", true_stats)
print("Distance:", distance(observed_stats, true_stats))

# --- Step 2: Run ABC ---
posterior_samples = abc_rejection(observed_stats, N=10000, epsilon=0.8, n_sim=20)

# --- Step 3: Plot Posterior ---
if len(posterior_samples) > 0:
    plt.figure(figsize=(10, 6))
    plt.scatter(posterior_samples[:, 0], posterior_samples[:, 1], alpha=0.4, label='Posterior samples')
    plt.axvline(true_kappa, color='red', linestyle='--', label='True κ')
    plt.axhline(true_theta, color='green', linestyle='--', label='True θ')
    plt.xlabel('κ (kappa)')
    plt.ylabel('θ (theta)')
    plt.title('ABC Posterior Samples for Heston Model')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("❌ No samples accepted. Try increasing epsilon or n_sim.")