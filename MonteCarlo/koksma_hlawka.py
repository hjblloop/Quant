import numpy as np
from scipy.stats import norm
import sobol_seq
import matplotlib.pyplot as plt

# === Option Parameters ===
S0 = 100
K = 100
r = 0.05
sigma = 0.2
T = 1.0
n_steps = 4
dt = T / n_steps
discount = np.exp(-r * T)

# === Simulation Parameters ===
sample_sizes = [2**i for i in range(6, 14)]  # 64 to 8192 samples
n_blocks = 10  # For QMC standard error estimate

# === Monte Carlo Pricing Function with Std. Error ===
def simulate_mc(N):
    z = np.random.normal(size=(N, n_steps))
    t = np.linspace(dt, T, n_steps).reshape(1, n_steps)
    W = np.sqrt(t) * z
    S_paths = S0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)
    avg_S = np.mean(S_paths, axis=1)
    payoff = np.maximum(avg_S - K, 0)
    prices = discount * payoff
    return prices.mean(), prices.std(ddof=1) / np.sqrt(N)

# === Quasi-Monte Carlo Pricing Function with Block Std. Error ===
def simulate_qmc(N, blocks=10):
    block_size = N // blocks
    sobol_points = sobol_seq.i4_sobol_generate(n_steps, N)
    norm_inv = norm.ppf(sobol_points)
    t = np.linspace(dt, T, n_steps).reshape(1, n_steps)

    payoffs = []
    for i in range(blocks):
        block = norm_inv[i*block_size:(i+1)*block_size]
        W = np.sqrt(t) * block
        S_paths = S0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)
        avg_S = np.mean(S_paths, axis=1)
        payoff = np.maximum(avg_S - K, 0)
        prices = discount * payoff
        payoffs.append(prices.mean())

    payoffs = np.array(payoffs)
    return payoffs.mean(), payoffs.std(ddof=1) / np.sqrt(blocks)

# === Run Simulations ===
mc_means, mc_errors = [], []
qmc_means, qmc_errors = [], []

for N in sample_sizes:
    mc_mean, mc_err = simulate_mc(N)
    qmc_mean, qmc_err = simulate_qmc(N)

    mc_means.append(mc_mean)
    mc_errors.append(mc_err)
    qmc_means.append(qmc_mean)
    qmc_errors.append(qmc_err)

# === Plotting ===
plt.figure(figsize=(10, 6))

# Plot MC
mc_means = np.array(mc_means)
mc_errors = np.array(mc_errors)
plt.plot(sample_sizes, mc_means, label='Monte Carlo', marker='o')
plt.fill_between(sample_sizes, mc_means - mc_errors, mc_means + mc_errors, alpha=0.2)

# Plot QMC
qmc_means = np.array(qmc_means)
qmc_errors = np.array(qmc_errors)
plt.plot(sample_sizes, qmc_means, label='Quasi-Monte Carlo (Sobol)', marker='s')
plt.fill_between(sample_sizes, qmc_means - qmc_errors, qmc_means + qmc_errors, alpha=0.2)

plt.xscale('log', base=2)
plt.xlabel('Number of Samples (log scale)')
plt.ylabel('Estimated Option Price')
plt.title('Asian Call Option Pricing: MC vs QMC with Error Bands')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()