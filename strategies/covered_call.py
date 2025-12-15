import matplotlib.pyplot as plt
import numpy as np

# 1. Strategy Parameters
S0 = 100        # Initial Stock Purchase Price
K = 105         # Strike Price (usually slightly higher than current price)
Premium = 5     # Premium received for selling the call
ST = np.linspace(80, 130, 500) # Range of Stock Prices at Expiration

# 2. Calculate Payoffs (Profit/Loss)
# Component A: Long Stock (You own the shares)
# Profit = Value at End - Initial Cost
profit_stock = ST - S0

# Component B: Short Call (You sold the option)
# Payoff = Premium - Max(Share Price - Strike, 0)
profit_short_call = Premium - np.maximum(ST - K, 0)

# Total Strategy: Covered Call (Sum of A + B)
profit_covered_call = profit_stock + profit_short_call

# 3. Plotting
# Set a light background for the plot area to make colors pop
plt.figure(figsize=(12, 7), facecolor='#f0f0f5')
ax = plt.gca()
ax.set_facecolor('#fcfcff')

# Define a more vibrant color palette
stock_color = '#6a0dad'      # Deep Purple
call_color = '#ff8c00'       # Dark Orange
covered_color = '#007bff'    # Bright Blue
profit_fill = '#28a745'      # Vivid Green
loss_fill = '#dc3545'        # Vivid Red
text_color = '#343a40'       # Dark Charcoal

# --- Plot the Individual Components (Dashed) ---
plt.plot(ST, profit_stock, label='Long Stock (Component A)', 
         color=stock_color, linestyle='--', linewidth=1.5, alpha=0.6)
plt.plot(ST, profit_short_call, label='Short Call (Component B)', 
         color=call_color, linestyle='--', linewidth=1.5, alpha=0.6)

# --- Plot the Combined Strategy (Thick/Solid) ---
plt.plot(ST, profit_covered_call, label='Covered Call (Result)', 
         color=covered_color, linewidth=3.5)

# 4. Add "Neat" Visuals
plt.axhline(0, color='black', linewidth=1.2) # Zero Line
plt.axvline(K, color='grey', linestyle=':', linewidth=1.2) # Strike Price Line

# Fill Profit/Loss Zones with more vibrant colors
plt.fill_between(ST, profit_covered_call, 0, where=(profit_covered_call >= 0), 
                 color=profit_fill, alpha=0.2, interpolate=True)
plt.fill_between(ST, profit_covered_call, 0, where=(profit_covered_call < 0), 
                 color=loss_fill, alpha=0.2, interpolate=True)

# 5. Annotations to make it "Fully Understandable"

# Breakeven Point
breakeven_price = S0 - Premium
plt.scatter([breakeven_price], [0], color=loss_fill, s=80, zorder=5, edgecolors='black')
plt.annotate(f'Breakeven\n(${breakeven_price})', 
             xy=(breakeven_price, 0), xytext=(breakeven_price-6, 8),
             arrowprops=dict(facecolor=text_color, arrowstyle='->', lw=1.5), ha='center', color=text_color, fontweight='bold')

# Max Profit Cap
max_profit = (K - S0) + Premium
plt.scatter([K], [max_profit], color=profit_fill, s=80, zorder=5, edgecolors='black')
plt.text(K + 2, max_profit, f'Max Profit Capped at ${max_profit}\n(Stock Gain + Premium)', 
         color=profit_fill, fontweight='bold', va='center', fontsize=11)

# The "Cushion" Explanation
plt.annotate('Downside Protection\n(The Premium cushions the loss)', 
             xy=(98, -2), xytext=(85, -12),
             arrowprops=dict(facecolor=stock_color, arrowstyle='->', connectionstyle="arc3,rad=.2", lw=1.5, color=stock_color),
             color=stock_color, fontweight='bold')

# 6. Final Polish
plt.title(f'Covered Call Analysis\nBuy Stock @ ${S0} + Sell Call (Strike ${K}) for ${Premium}', fontsize=16, color=text_color, fontweight='bold')
plt.xlabel('Stock Price at Expiration ($S_T$)', fontsize=12, color=text_color, fontweight='bold')
plt.ylabel('Profit / Loss ($)', fontsize=12, color=text_color, fontweight='bold')
plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
plt.grid(True, alpha=0.3, color='grey', linestyle='--')
plt.xlim(80, 130)
plt.ylim(-20, 20)

plt.tight_layout()
plt.show()