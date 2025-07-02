import numpy as np
from scipy.stats import norm
import sobol_seq
import matplotlib.pyplot as plt

# === Option Parameters ===
S0 = 100       # Initial price
K = 100        # Strike price
r = 0.05       # Risk-free rate
sigma = 0.2    # Volatility
T = 1.0        # Maturity
n_steps = 4    # Number of averaging points
dt = T / n_steps
discount = np.exp(-r * T)

# === Simulation Parameters ===
sample_sizes = [2**i for i in range(6, 14)]  # From 64 to 8192 samples

def simulate_asian_option_mc(N):
    z = np.random.normal(size=(N, n_steps))
    t = np.linspace(dt, T, n_steps)
    t = t.reshape((1, n_steps))

    W = np.sqrt(t) * z
    S_paths = S0 * np.exp((r - 0.5 * sigma ** 2) * t + sigma * W)
    avg_S = np.mean(S_paths, axis=1)
    payoff = np.maximum(avg_S - K, 0)
    return discount * np.mean(payoff)

def simulate_asian_option_qmc(N):
    sobol_points = sobol_seq.i4_sobol_generate(n_steps, N)
    norm_inv = norm.ppf(sobol_points)
    t = np.linspace(dt, T, n_steps)
    t = t.reshape((1, n_steps))

    W = np.sqrt(t) * norm_inv
    S_paths = S0 * np.exp((r - 0.5 * sigma ** 2) * t + sigma * W)
    avg_S = np.mean(S_paths, axis=1)
    payoff = np.maximum(avg_S - K, 0)
    return discount * np.mean(payoff)

# === Run Simulations ===
mc_results = []
qmc_results = []

for N in sample_sizes:
    price_mc = simulate_asian_option_mc(N)
    price_qmc = simulate_asian_option_qmc(N)
    mc_results.append(price_mc)
    qmc_results.append(price_qmc)

# === Plotting ===
plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, mc_results, label='Monte Carlo', marker='o')
plt.plot(sample_sizes, qmc_results, label='Quasi-Monte Carlo (Sobol)', marker='s')
plt.axhline(y=qmc_results[-1], color='gray', linestyle='--', label='QMC Final Estimate')
plt.xscale('log', base=2)
plt.xlabel('Number of Samples (log scale)')
plt.ylabel('Estimated Option Price')
plt.title('Convergence of Asian Option Price (MC vs QMC)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()