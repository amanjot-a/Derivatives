import matplotlib.pyplot as plt
import numpy as np

# 1. Parameters
ST = np.linspace(0, 200, 400)  # Range of stock prices at maturity
K = 100     # Strike Price
c0 = 20     # Premium received for selling the call (Option Price)

# 2. Calculations
# Short Call Payoff = - Max(ST - K, 0)
# This is the value of the option contract itself at expiration (negative for the seller)
payoff_short_call = -np.maximum(ST - K, 0)

# Short Call Profit = Payoff + Premium Received
profit_short_call = payoff_short_call + c0

# 3. Plotting
plt.figure(figsize=(10, 6))

# Plot Payoff (The dashed line shows the pure option value obligation)
plt.plot(ST, payoff_short_call, label='Short Call Payoff (No Premium)', 
         linestyle='--', linewidth=1.5, color='orange', alpha=0.7)

# Plot Profit (The solid line shows your actual P&L)
plt.plot(ST, profit_short_call, label=f'Short Call Profit (Premium={c0})', 
         linewidth=2.5, color='red')

# 4. Visual formatting (Axis lines, markers)
plt.axhline(0, color='black', linewidth=1) # Zero line
plt.axvline(K, color='gray', linestyle=':', linewidth=1) # Strike Price line

# Highlight the Breakeven Point (Strike + Premium)
breakeven = K + c0
plt.scatter([breakeven], [0], color='black', zorder=5)
plt.annotate(f'Breakeven\n(${breakeven})', xy=(breakeven, 0), xytext=(breakeven+10, 10),
             arrowprops=dict(facecolor='black', shrink=0.05))

# Highlight Max Profit (The Premium)
plt.text(5, c0 + 2, f'Max Profit = Premium (${c0})', color='green', fontweight='bold')

plt.title(f'Short Call Strategy (Strike K={K})')
plt.xlabel('Stock Price at Maturity ($S_T$)')
plt.ylabel('Profit / Loss')
plt.legend()
plt.grid(True, alpha=0.3)

# Set limits to match your previous style
plt.xlim(0, 200)
plt.ylim(-100, 50) 

plt.show()