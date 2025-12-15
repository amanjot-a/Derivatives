import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# PAPER-STYLE SINGLE-PERIOD BINOMIAL CPT
# =====================================================
def binomial_CPT_paper(S0, K, r, T, u, d, option="call"):

    # Stock prices
    Su = S0 * u
    Sd = S0 * d

    # Payoffs
    if option == "call":
        Cu = max(Su - K, 0)
        Cd = max(Sd - K, 0)
    else:  # put
        Cu = max(K - Su, 0)
        Cd = max(K - Sd, 0)

    # Simple interest factor (paper convention)
    R = 1 + r * T

    # Risk-neutral probability (rounded like exams)
    p = round((R - d) / (u - d), 2)

    # Expected payoff
    expected_payoff = p * Cu + (1 - p) * Cd

    # Discount ONCE, round at the end
    price = round(expected_payoff / R, 2)

    # Hedge ratio (exact fraction, then rounded)
    delta = round((Cu - Cd) / (Su - Sd), 2)

    # Bond position (from replication identity)
    B = round(price - delta * S0, 2)

    return {
        "S0": S0,
        "Su": Su,
        "Sd": Sd,
        "Cu": Cu,
        "Cd": Cd,
        "R": R,
        "p": p,
        "Expected Payoff": expected_payoff,
        "Delta": delta,
        "Bond": B,
        "Price": price
    }

# =====================================================
# PRINT CPT (EXAM FORMAT)
# =====================================================
def print_CPT(results, option):

    print("\n" + "="*35)
    print(f"PAPER-STYLE CPT ({option.upper()})")
    print("="*35)

    print(f"S0: {results['S0']}")
    print(f"Su = S0·u: {results['Su']}")
    print(f"Sd = S0·d: {results['Sd']}\n")

    print(f"Cu: {results['Cu']}")
    print(f"Cd: {results['Cd']}\n")

    print(f"R = 1 + rT: {results['R']}")
    print(f"Risk-neutral p: {results['p']}\n")

    print(f"Δ (hedge ratio): {results['Delta']}")
    print(f"Bond position B: {results['Bond']}\n")

    print(f"OPTION PRICE: {results['Price']}")
    print("="*35)

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":

    S0 = 100
    K = 110
    r = 0.05
    T = 1
    u = 1.6
    d = 0.7

    # CALL
    call = binomial_CPT_paper(S0, K, r, T, u, d, "call")
    print_CPT(call, "call")

    # PUT
    put = binomial_CPT_paper(S0, K, r, T, u, d, "put")
    print_CPT(put, "put")
