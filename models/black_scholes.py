#!/usr/bin/env python3
"""
Black-Scholes Analytics Dashboard (dark-mode)
- Produces PNGs, a multi-panel PDF, and a CSV sample
- Marks current Spot and Strike on appropriate charts
- Optionally creates interactive Plotly HTML (if plotly installed)
"""

from math import log, sqrt, exp
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import norm
import os
import csv

# ---------- Black-Scholes functions ----------
def bs_call_put(S, K, r, sigma, T):
    """
    Return tuple:
    (call_price, put_price, call_delta, put_delta, gamma, vega, call_theta_per_day, put_theta_per_day)
    Theta returned is per-day.
    """
    if T <= 0:
        call = max(S - K, 0.0)
        put  = max(K - S, 0.0)
        call_delta = 1.0 if S > K else 0.0
        put_delta  = call_delta - 1.0
        gamma = 0.0
        vega  = 0.0
        call_theta = 0.0
        put_theta  = 0.0
        return call, put, call_delta, put_delta, gamma, vega, call_theta, put_theta

    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    put  = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    call_delta = norm.cdf(d1)
    put_delta  = call_delta - 1.0

    pdf_d1 = norm.pdf(d1)
    gamma = pdf_d1 / (S * sigma * sqrt(T))
    vega  = S * pdf_d1 * sqrt(T)

    call_theta_annual = (-S * pdf_d1 * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * norm.cdf(d2)
    put_theta_annual  = (-S * pdf_d1 * sigma) / (2 * sqrt(T)) + r * K * exp(-r * T) * norm.cdf(-d2)

    return call, put, call_delta, put_delta, gamma, vega, call_theta_annual/365.0, put_theta_annual/365.0

# ---------- Inputs ----------
S_center = 82000.0         # current spot to mark on charts
K = 93800.0                # strike to mark
r = 0.05                   # risk-free rate (decimal)
sigma = 0.50               # volatility (decimal)

expiry = datetime(2026, 1, 10, 14, 0, 0)
now = datetime.now()
T_ref = max((expiry - now).total_seconds() / (365 * 24 * 3600), 1e-8)  # years (non-zero floor)

outdir = "./bs_dashboard_outputs"
os.makedirs(outdir, exist_ok=True)

plt.style.use('dark_background')  # dark theme as requested

# ---------- Helper to save a figure ----------
def save_fig(fig, filename_png):
    fig.savefig(filename_png, dpi=150, bbox_inches='tight')
    print("Saved:", filename_png)

# ---------- 1) Premium vs Spot ----------
S_min = S_center * 0.7
S_max = S_center * 1.3
S_range = np.linspace(S_min, S_max, 400)
calls = np.empty_like(S_range)
puts  = np.empty_like(S_range)

for i, S in enumerate(S_range):
    c, p, *_ = bs_call_put(S, K, r, sigma, T_ref)
    calls[i] = c
    puts[i] = p

fig1, ax1 = plt.subplots(figsize=(9,6))
ax1.plot(S_range, calls, label='Call Price')
ax1.plot(S_range, puts,  label='Put Price')
# mark current spot and strike
c_spot_call, c_spot_put, cd_spot, pd_spot, _, _, cth_spot, pth_spot = bs_call_put(S_center, K, r, sigma, T_ref)
ax1.axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
ax1.annotate(f'Spot={S_center:.0f}\nCall={c_spot_call:.2f}\nPut={c_spot_put:.2f}',
             xy=(S_center, max(c_spot_call, c_spot_put)), xytext=(10, -60),
             textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax1.axvline(K, linestyle=':', linewidth=1, alpha=0.7)
ax1.annotate(f'Strike={K:.0f}', xy=(K, 0), xytext=(-60, 20), textcoords='offset points',
             bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax1.set_xlabel('Spot Price (S)')
ax1.set_ylabel('Option Premium')
ax1.set_title('Option Premium vs Spot Price (Call & Put)')
ax1.legend()
ax1.grid(alpha=0.25)
png1 = os.path.join(outdir, "premium_vs_spot.png")
save_fig(fig1, png1)

# ---------- 2) Delta vs Spot ----------
call_delta = np.empty_like(S_range)
put_delta  = np.empty_like(S_range)
gamma_arr  = np.empty_like(S_range)

for i, S in enumerate(S_range):
    _, _, cd, pd, gm, _, _, _ = bs_call_put(S, K, r, sigma, T_ref)
    call_delta[i] = cd
    put_delta[i]  = pd
    gamma_arr[i]  = gm

fig2, ax2 = plt.subplots(figsize=(9,6))
ax2.plot(S_range, call_delta, label='Call Delta')
ax2.plot(S_range, put_delta,  label='Put Delta')
ax2.axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
cd_at_spot = np.interp(S_center, S_range, call_delta)
pd_at_spot = np.interp(S_center, S_range, put_delta)
ax2.annotate(f'CallΔ={cd_at_spot:.3f}\nPutΔ={pd_at_spot:.3f}', xy=(S_center, cd_at_spot), xytext=(10, -40),
             textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax2.set_xlabel('Spot Price (S)')
ax2.set_ylabel('Delta')
ax2.set_title('Delta vs Spot Price')
ax2.legend()
ax2.grid(alpha=0.25)
png2 = os.path.join(outdir, "delta_vs_spot.png")
save_fig(fig2, png2)

# ---------- 3) Gamma vs Spot ----------
fig3, ax3 = plt.subplots(figsize=(9,6))
ax3.plot(S_range, gamma_arr, label='Gamma')
ax3.axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
gm_at_spot = np.interp(S_center, S_range, gamma_arr)
ax3.annotate(f'Gamma@S={S_center:.0f} = {gm_at_spot:.6e}', xy=(S_center, gm_at_spot), xytext=(10, -40),
             textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax3.set_xlabel('Spot Price (S)')
ax3.set_ylabel('Gamma')
ax3.set_title('Gamma vs Spot Price')
ax3.legend()
ax3.grid(alpha=0.25)
png3 = os.path.join(outdir, "gamma_vs_spot.png")
save_fig(fig3, png3)

# ---------- 4) Vega vs Volatility ----------
sigma_range = np.linspace(0.01, 1.2, 300)
vega_arr = np.empty_like(sigma_range)
for i, sig in enumerate(sigma_range):
    _, _, _, _, _, vg, _, _ = bs_call_put(S_center, K, r, sig, T_ref)
    vega_arr[i] = vg

fig4, ax4 = plt.subplots(figsize=(9,6))
ax4.plot(sigma_range, vega_arr, label='Vega')
# annotate current sigma
vg_at_sigma = np.interp(sigma, sigma_range, vega_arr)
ax4.axvline(sigma, linestyle='--', linewidth=1, alpha=0.8)
ax4.annotate(f'sigma={sigma:.2f}\nVega={vg_at_sigma:.1f}', xy=(sigma, vg_at_sigma), xytext=(10, -40),
             textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax4.set_xlabel('Volatility (sigma, decimal)')
ax4.set_ylabel('Vega (per 1 vol point)')
ax4.set_title(f'Vega vs Volatility (for S = {S_center:.0f})')
ax4.legend()
ax4.grid(alpha=0.25)
png4 = os.path.join(outdir, "vega_vs_vol.png")
save_fig(fig4, png4)

# ---------- 5) Theta vs Time to Expiry (days) ----------
# Show 1 day to 1 year (or T_ref if > 1y, we still show up to 365 days for clarity)
days_max = max(365, int(max(T_ref*365, 30)))
days = np.linspace(1, days_max, 300)
call_theta_arr = np.empty_like(days)
put_theta_arr  = np.empty_like(days)
for i, d in enumerate(days):
    T = d / 365.0
    _, _, _, _, _, _, cth, pth = bs_call_put(S_center, K, r, sigma, T)
    call_theta_arr[i] = cth
    put_theta_arr[i]  = pth

fig5, ax5 = plt.subplots(figsize=(9,6))
ax5.plot(days, call_theta_arr, label='Call Theta (per day)')
ax5.plot(days, put_theta_arr,  label='Put Theta (per day)')
# annotate T_ref point
days_ref = max(1, T_ref*365)
ct_ref = np.interp(days_ref, days, call_theta_arr)
pt_ref = np.interp(days_ref, days, put_theta_arr)
ax5.axvline(days_ref, linestyle='--', linewidth=1, alpha=0.8)
ax5.annotate(f'T_ref={days_ref:.0f}d\nCallθ={ct_ref:.2f}\nPutθ={pt_ref:.2f}', xy=(days_ref, ct_ref), xytext=(10, -60),
             textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax5.set_xlabel('Time to expiry (days)')
ax5.set_ylabel('Theta (per day)')
ax5.set_title(f'Theta vs Time to Expiry (for S = {S_center:.0f})')
ax5.legend()
ax5.grid(alpha=0.25)
png5 = os.path.join(outdir, "theta_vs_time.png")
save_fig(fig5, png5)

# ---------- 6) Rho vs Interest Rate ----------
r_range = np.linspace(0.0, 0.20, 200)
call_rho_arr = np.empty_like(r_range)
put_rho_arr  = np.empty_like(r_range)
eps = 1e-5
for i, rr in enumerate(r_range):
    c_up, p_up, *_ = bs_call_put(S_center, K, rr + eps, sigma, T_ref)
    c_dn, p_dn, *_ = bs_call_put(S_center, K, rr - eps, sigma, T_ref)
    call_rho_arr[i] = (c_up - c_dn) / (2 * eps)
    put_rho_arr[i]  = (p_up - p_dn) / (2 * eps)

fig6, ax6 = plt.subplots(figsize=(9,6))
ax6.plot(r_range, call_rho_arr, label='Call Rho')
ax6.plot(r_range, put_rho_arr, label='Put Rho')
# annotate at current r
rho_call_at_r = np.interp(r, r_range, call_rho_arr)
rho_put_at_r  = np.interp(r, r_range, put_rho_arr)
ax6.axvline(r, linestyle='--', linewidth=1, alpha=0.8)
ax6.annotate(f'r={r:.2f}\nCallRho={rho_call_at_r:.1f}\nPutRho={rho_put_at_r:.1f}', xy=(r, rho_call_at_r),
             xytext=(10, -60), textcoords='offset points', bbox=dict(facecolor='black', alpha=0.6), fontsize=9)
ax6.set_xlabel('Risk-free rate (r)')
ax6.set_ylabel('Rho (sensitivity to r)')
ax6.set_title(f'Rho vs Interest Rate (for S = {S_center:.0f})')
ax6.legend()
ax6.grid(alpha=0.25)
png6 = os.path.join(outdir, "rho_vs_r.png")
save_fig(fig6, png6)

# ---------- Save a multi-page PDF with all six plots (2 pages, 3 panels each) ----------
pdf_path = os.path.join(outdir, "bs_dashboard_multi_panel.pdf")
with PdfPages(pdf_path) as pdf:
    # Page 1: plots 1-3 (arrange vertically)
    fig_page1, axes = plt.subplots(3, 1, figsize=(10, 16))
    # Premium
    axes[0].plot(S_range, calls, label='Call Price')
    axes[0].plot(S_range, puts,  label='Put Price')
    axes[0].axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
    axes[0].axvline(K, linestyle=':', linewidth=1, alpha=0.7)
    axes[0].set_title('Option Premium vs Spot Price (Call & Put)')
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    # Delta
    axes[1].plot(S_range, call_delta, label='Call Delta')
    axes[1].plot(S_range, put_delta,  label='Put Delta')
    axes[1].axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
    axes[1].set_title('Delta vs Spot Price')
    axes[1].legend()
    axes[1].grid(alpha=0.25)
    # Gamma
    axes[2].plot(S_range, gamma_arr, label='Gamma')
    axes[2].axvline(S_center, linestyle='--', linewidth=1, alpha=0.8)
    axes[2].set_title('Gamma vs Spot Price')
    axes[2].legend()
    axes[2].grid(alpha=0.25)

    pdf.savefig(fig_page1)
    plt.close(fig_page1)

    # Page 2: plots 4-6
    fig_page2, axes2 = plt.subplots(3, 1, figsize=(10, 16))
    # Vega
    axes2[0].plot(sigma_range, vega_arr, label='Vega')
    axes2[0].axvline(sigma, linestyle='--', linewidth=1, alpha=0.8)
    axes2[0].set_title(f'Vega vs Volatility (for S = {S_center:.0f})')
    axes2[0].legend()
    axes2[0].grid(alpha=0.25)
    # Theta
    axes2[1].plot(days, call_theta_arr, label='Call Theta (per day)')
    axes2[1].plot(days, put_theta_arr,  label='Put Theta (per day)')
    axes2[1].axvline(days_ref, linestyle='--', linewidth=1, alpha=0.8)
    axes2[1].set_title(f'Theta vs Time to Expiry (for S = {S_center:.0f})')
    axes2[1].legend()
    axes2[1].grid(alpha=0.25)
    # Rho
    axes2[2].plot(r_range, call_rho_arr, label='Call Rho')
    axes2[2].plot(r_range, put_rho_arr, label='Put Rho')
    axes2[2].axvline(r, linestyle='--', linewidth=1, alpha=0.8)
    axes2[2].set_title(f'Rho vs Interest Rate (for S = {S_center:.0f})')
    axes2[2].legend()
    axes2[2].grid(alpha=0.25)

    pdf.savefig(fig_page2)
    plt.close(fig_page2)

print("Multi-panel PDF saved to:", pdf_path)

# ---------- Save CSV of ATM sweep ----------
csv_path = os.path.join(outdir, "sample_atm.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["S", "CallPrice", "PutPrice", "CallDelta", "PutDelta", "Gamma", "Vega", "CallTheta_per_day", "PutTheta_per_day"])
    for S in np.linspace(S_center*0.9, S_center*1.1, 21):
        c, p, cd, pd, gm, vg, cth, pth = bs_call_put(S, K, r, sigma, T_ref)
        writer.writerow([S, c, p, cd, pd, gm, vg, cth, pth])
print("CSV sample saved to:", csv_path)

# ---------- Optional: interactive Plotly HTML export (if plotly installed) ----------
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    html_out = os.path.join(outdir, "bs_dashboard_interactive.html")
    # Simple interactive figure with premium vs spot and delta vs spot subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Premium vs Spot (Call & Put)", "Delta vs Spot"))
    fig.add_trace(go.Scatter(x=S_range, y=calls, name="Call Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=S_range, y=puts, name="Put Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=S_range, y=call_delta, name="Call Delta"), row=2, col=1)
    fig.add_trace(go.Scatter(x=S_range, y=put_delta, name="Put Delta"), row=2, col=1)
    # Markers
    fig.add_vline(x=S_center, line_dash="dash", annotation_text=f"Spot={S_center:.0f}")
    fig.add_vline(x=K, line_dash="dot", annotation_text=f"Strike={K:.0f}")
    fig.update_layout(template="plotly_dark", height=900)
    fig.write_html(html_out)
    print("Interactive HTML exported to:", html_out)
except Exception:
    print("Plotly not installed or failed — skipping interactive HTML export (optional).")

print("\nAll outputs written to folder:", os.path.abspath(outdir))
print("Done.")
