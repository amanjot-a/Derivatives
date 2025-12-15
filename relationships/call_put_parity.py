import numpy as np
import matplotlib.pyplot as plt

# Parameters
S0 = 100
K = 95
put_premium = 4
call_premium = 4  # for symmetry example
r = 0.05
T = 1
PV_K = K / np.exp(r * T)

# Range of stock prices at expiration
S_T = np.linspace(50, 150, 300)

# Protective Put Payoff
stock_payoff = S_T - S0
put_payoff = np.maximum(K - S_T, 0) - put_premium
protective_put_total = stock_payoff + put_payoff

# Fiduciary Call Payoff
call_payoff = np.maximum(S_T - K, 0) - call_premium
bond_payoff = PV_K * np.exp(r * T) - PV_K  # zero net at expiry
fiduciary_call_total = call_payoff + (K - K)  # simplified payoff matches call payoff

# Plot Protective Put
plt.figure(figsize=(8,5))
plt.plot(S_T, protective_put_total, label="Protective Put Payoff")
plt.axhline(0)
plt.title("Protective Put Payoff")
plt.xlabel("Stock Price at Expiration")
plt.ylabel("Profit / Loss")
plt.legend()
plt.grid(True)
plt.show()

# Plot Fiduciary Call
plt.figure(figsize=(8,5))
plt.plot(S_T, fiduciary_call_total, label="Fiduciary Call Payoff")
plt.axhline(0)
plt.title("Fiduciary Call Payoff")
plt.xlabel("Stock Price at Expiration")
plt.ylabel("Profit / Loss")
plt.legend()
plt.grid(True)
plt.show()
