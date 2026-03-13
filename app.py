import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Interactive Ricardian Trade Model")
st.markdown("Enter the parameters for both countries to see the PPFs, comparative advantages, and optional utility equilibrium.")

# --- Sidebar Numerical Inputs ---
st.sidebar.header("🏠 Home Country")
L_h = st.sidebar.number_input("Labor Force (L)", min_value=1, value=100)
mpl_c_h = st.sidebar.number_input("MPL Cheese", min_value=0.1, value=4.0, step=0.5)
mpl_w_h = st.sidebar.number_input("MPL Wine", min_value=0.1, value=2.0, step=0.5)

st.sidebar.header("🌍 Foreign Country")
L_f = st.sidebar.number_input("Labor Force (L*)", min_value=1, value=100)
mpl_c_f = st.sidebar.number_input("MPL* Cheese", min_value=0.1, value=1.0, step=0.5)
mpl_w_f = st.sidebar.number_input("MPL* Wine", min_value=0.1, value=5.0, step=0.5)

# --- Utility Selection & World Price ---
st.sidebar.divider()
use_utility = st.sidebar.checkbox("Enable Utility Analysis (Cobb-Douglas)")

# --- Logic & Calculations ---
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

oc_c_h = mpl_w_h / mpl_c_h
oc_c_f = mpl_w_f / mpl_c_f
are_costs_equal = round(oc_c_h, 4) == round(oc_c_f, 4)

# Dynamic Price Slider (Only shows if utility is enabled and trade is possible)
p_world = (oc_c_h + oc_c_f) / 2 # Default
if use_utility and not are_costs_equal:
    p_min, p_max = sorted([oc_c_h, oc_c_f])
    p_world = st.sidebar.slider("World Price ($P_C/P_W$)", 
                                 min_value=float(p_min), 
                                 max_value=float(p_max), 
                                 value=float(p_world))

# --- Graphing ---
fig, ax = plt.subplots(figsize=(10, 7))

# Plot PPFs
ax.plot([0, max_c_h], [max_w_h, 0], 'b-', label='Home PPF', linewidth=3)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-', label='Foreign PPF', linewidth=3)

# Utility Logic: Budget Lines & Consumption Points
if use_utility and not are_costs_equal:
    # Home Equilibrium
    if oc_c_h < oc_c_f: # Specializes in Cheese
        inc_h = max_c_h * p_world
        c_h, w_h = (0.5 * inc_h / p_world), (0.5 * inc_h)
        ax.plot([0, inc_h/p_world], [inc_h, 0], 'b--', alpha=0.6, label='Home Budget Line')
    else: # Specializes in Wine
        inc_h = max_w_h
        c_h, w_h = (0.5 * inc_h / p_world), (0.5 * inc_h)
        ax.plot([0, inc_h/p_world], [inc_h, 0], 'b--', alpha=0.6, label='Home Budget Line')
    
    # Foreign Equilibrium
    if oc_c_f < oc_c_h: # Specializes in Cheese
        inc_f = max_c_f * p_world
        c_f, w_f = (0.5 * inc_f / p_world), (0.5 * inc_f)
        ax.plot([0, inc_f/p_world], [inc_f, 0], 'r--', alpha=0.6, label='Foreign Budget Line')
    else: # Specializes in Wine
        inc_f = max_w_f
        c_f, w_f = (0.5 * inc_f / p_world), (0.5 * inc_f)
        ax.plot([0, inc_f/p_world], [inc_f, 0], 'r--', alpha=0.6, label='Foreign Budget Line')

    # Consumption Dots & Indifference Curves
    ax.scatter([c_h, c_f], [w_h, w_f], color=['blue', 'red'], zorder=5)
    c_space = np.linspace(0.1, max(max_c_h, max_c_f)*1.5, 100)
    u_h, u_f = (c_h**0.5 * w_h**0.5), (c_f**0.5 * w_f**0.5)
    ax.plot(c_space, (u_h**2)/c_space, 'b:', alpha=0.4)
    ax.plot(c_space, (u_f**2)/c_space, 'r:', alpha=0.4)

# Styling
limit = max(max_c_h, max_w_h, max_c_f, max_w_f) * 1.2
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)
ax.set_xlabel("Quantity of Cheese")
ax.set_ylabel("Quantity of Wine")
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
st.pyplot(fig)

# --- Analysis Dashboard (Always Visible) ---
st.header("Comparative Advantage Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Home Country")
    st.write(f"Opportunity Cost of 1 Cheese: **{oc_c_h:.2f} Wine**")
    if are_costs_equal:
        st.warning("No Comparative Advantage")
    elif oc_c_h < oc_c_f:
        st.success("✅ Comparative Advantage: **Cheese**")
    else:
        st.success("✅ Comparative Advantage: **Wine**")

with col2:
    st.subheader("Foreign Country")
    st.write(f"Opportunity Cost of 1 Cheese: **{oc_c_f:.2f} Wine**")
    if are_costs_equal:
        st.warning("No Comparative Advantage")
    elif oc_c_f < oc_c_h:
        st.success("✅ Comparative Advantage: **Cheese**")
    else:
        st.success("✅ Comparative Advantage: **Wine**")

st.divider()

# Terms of Trade logic
if are_costs_equal:
    st.error("🚫 **No Trade Possible**")
    st.write("Since opportunity costs are identical, there is no incentive for trade.")
else:
    lower_bound, upper_bound = min(oc_c_h, oc_c_f), max(oc_c_h, oc_c_f)
    st.info(f"💡 In free trade, the world (relative) price of Cheese ($P_C/P_W$) will be between **{lower_bound:.2f}** and **{upper_bound:.2f}**.")

# --- Utility Results (Conditional) ---
if use_utility and not are_costs_equal:
    st.subheader("Consumption & Utility Equilibrium")
    u_col1, u_col2 = st.columns(2)
    with u_col1:
        st.write(f"🏠 **Home consumes:** {c_h:.1f}C, {w_h:.1f}W")
        st.write(f"**Utility (U):** {u_h:.2f}")
    with u_col2:
        st.write(f"🌍 **Foreign consumes:** {c_f:.1f}C, {w_f:.1f}W")
        st.write(f"**Utility (U*):** {u_f:.2f}")
