import numpy as np
import streamlit as st

st.title("Monte Carlo Option Pricer with Greeks")

st.sidebar.header("Input Parameters")
S0 = st.sidebar.number_input("Initial Stock Price (S₀)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Time to Maturity (T in years)", value=1.0, min_value=0.01)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
n_sim = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=500000, value=100000, step=1000)
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])

def monte_carlo_price(S0, K, T, r, sigma, n_sim, option_type="Call"):
    Z = np.random.randn(n_sim)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    if option_type == "Call":
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)
    return np.exp(-r * T) * np.mean(payoffs)

def compute_greeks(S0, K, T, r, sigma, n_sim, option_type):
    # Price base
    base_price = monte_carlo_price(S0, K, T, r, sigma, n_sim, option_type)

    # Finite difference bump sizes
    dS = 0.01 * S0
    dSigma = 0.01
    dT = 1 / 365  # 1 day
    dr = 0.001

    # Delta
    price_up = monte_carlo_price(S0 + dS, K, T, r, sigma, n_sim, option_type)
    price_down = monte_carlo_price(S0 - dS, K, T, r, sigma, n_sim, option_type)
    delta = (price_up - price_down) / (2 * dS)

    # Gamma
    gamma = (price_up - 2 * base_price + price_down) / (dS ** 2)

    # Vega
    vega = (monte_carlo_price(S0, K, T, r, sigma + dSigma, n_sim, option_type) -
            monte_carlo_price(S0, K, T, r, sigma - dSigma, n_sim, option_type)) / (2 * dSigma)

    # Theta
    theta = (monte_carlo_price(S0, K, T - dT, r, sigma, n_sim, option_type) -
             base_price) / dT

    # Rho
    rho = (monte_carlo_price(S0, K, T, r + dr, sigma, n_sim, option_type) -
           monte_carlo_price(S0, K, T, r - dr, sigma, n_sim, option_type)) / (2 * dr)

    return base_price, delta, gamma, vega, theta, rho

if st.button("Calculate Option Price and Greeks"):
    with st.spinner("Running simulations..."):
        price, delta, gamma, vega, theta, rho = compute_greeks(S0, K, T, r, sigma, n_sim, option_type)

    st.success(f"{option_type} Option Price: {price:.4f}")

    st.subheader("Option Greeks:")
    st.markdown(f"- **Delta (Δ):** `{delta:.4f}`")
    st.markdown(f"- **Gamma (Γ):** `{gamma:.4f}`")
    st.markdown(f"- **Vega (ν):** `{vega:.4f}`")
    st.markdown(f"- **Theta (Θ):** `{theta:.4f}` per year")
    st.markdown(f"- **Rho (ρ):** `{rho:.4f}`")