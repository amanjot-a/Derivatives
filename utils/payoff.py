import matplotlib.pyplot as plt
import numpy as np

# Parameters (chosen to match the lecture screenshot: strike/forward = 100)
ST = np.linspace(0, 200, 400)
F0 = 100   # forward price / strike
K = 100
p0 = 25     # example put premium received for the short put (I'll state this explicitly)

# Payoffs at maturity (no premiums)
payoff_long_forward = ST - F0
payoff_short_put = -np.maximum(K - ST, 0)  # short put payoff = -put_payoff

# Profits including premium (example: short put receives premium p0)
profit_long_forward = payoff_long_forward  # forward typically has no upfront premium in payoff at T
profit_short_put = payoff_short_put + p0

plt.figure(figsize=(10,6))
plt.plot(ST, payoff_long_forward, label="Long Forward payoff (ST - F0)", linewidth=2)
plt.plot(ST, payoff_short_put, label="Short Put payoff (-max(K-ST,0))", linewidth=2, linestyle='--')
plt.plot(ST, profit_short_put, label=f"Short Put profit (payoff + premium p0={p0})", linewidth=2, linestyle=':')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(F0, color='gray', linewidth=0.8, linestyle=':')
plt.scatter([F0],[0], color='gray')
plt.text(F0+2, -8, f"Strike/Forward = {F0}", color='gray')

plt.xlabel("Underlying Price $S_T$")
plt.ylabel("Payoff / Profit")
plt.title("Long Forward vs Short Put — Payoffs and Example Profit (premium shown)")
plt.xlim(0,200)
plt.ylim(-120,120)
plt.legend()
plt.grid(alpha=0.3)
plt.show()
