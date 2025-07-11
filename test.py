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

true_kappa = 1.2
true_theta = 0.05
S, v = simulate_heston(true_kappa, true_theta)
returns = np.diff(np.log(S))
plt.plot(S)
plt.title("Simulated Price Path")
plt.show()
plt.plot(v)
plt.title("Simulated Variance Path")
plt.show()