import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Interactive Ricardian Trade Model")
st.markdown("Explore productivity, comparative advantage, and general equilibrium trade.")

# --- Sidebar Numerical Inputs ---
st.sidebar.header("🏠 Home Country")
L_h = st.sidebar.number_input("Labor Force (L)", min_value=1, value=100)
mpl_c_h = st.sidebar.number_input("MPL Cheese", min_value=0.1, value=4.0, step=0.5)
mpl_w_h = st.sidebar.number_input("MPL Wine", min_value=0.1, value=2.0, step=0.5)

st.sidebar.header("🌍 Foreign Country")
L_f = st.sidebar.number_input("Labor Force (L*)", min_value=1, value=100)
mpl_c_f = st.sidebar.number_input("MPL* Cheese", min_value=0.1, value=1.0, step=0.5)
mpl_w_f = st.sidebar.number_input("MPL* Wine", min_value=0.1, value=5.0, step=0.5)

st.sidebar.divider()
use_equilibrium = st.sidebar.checkbox("Show Utility & Market Clearing")

# --- Logic & Calculations ---
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

oc_c_h = mpl_w_h / mpl_c_h
oc_c_f = mpl_w_f / mpl_c_f
are_costs_equal = round(oc_c_h, 4) == round(oc_c_f, 4)

# Market Clearing Price Calculation
if not are_costs_equal:
    if oc_c_h < oc_c_f:
        world_c_supply, world_w_supply = max_c_h, max_w_f
    else:
        world_c_supply, world_w_supply = max_c_f, max_w_h
    
    p_clearing = world_w_supply / world_c_supply
    lower_b, upper_b = sorted([oc_c_h, oc_c_f])
    p_final = max(lower_b, min(p_clearing, upper_b))
else:
    p_final = oc_c_h

# --- Graphing ---
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot([0, max_c_h], [max_w_h, 0], 'b-', label='Home PPF', linewidth=3)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-', label='Foreign PPF', linewidth=3)

# Overlay Utility Analysis and Production Points
if use_equilibrium and not are_costs_equal:
    # Home Production & Consumption
    if oc_c_h < oc_c_f: # Specializes in Cheese
        prod_h = (max_c_h, 0)
        inc_h = max_c_h * p_final
    else: # Specializes in Wine
        prod_h = (0, max_w_h)
        inc_h = max_w_h
    
    c_h, w_h = (0.5 * inc_h / p_final), (0.5 * inc_h)
    ax.plot([0, inc_h/p_final], [inc_h, 0], 'b--', alpha=0.6, label='Home Budget Line')
    ax.scatter(prod_h[0], prod_h[1], color='blue', edgecolors='black', s=100, zorder=6)
    ax.text(prod_h[0], prod_h[1], '  Home production in trade', verticalalignment='bottom', fontweight='bold', color='blue')
    
    # Foreign Production & Consumption
    if oc_c_f < oc_c_h: # Specializes in Cheese
        prod_f = (max_c_f, 0)
        inc_f = max_c_f * p_final
    else: # Specializes in Wine
        prod_f = (0, max_w_f)
        inc_f = max_w_f
        
    c_f, w_f = (0.5 * inc_f / p_final), (0.5 * inc_f)
    ax.plot([0, inc_f/p_final], [inc_f, 0], 'r--', alpha=0.6, label='Foreign Budget Line')
    ax.scatter(prod_f[0], prod_f[1], color='red', edgecolors='black', s=100, zorder=6)
    ax.text(prod_f[0], prod_f[1], '  Foreign production in trade', verticalalignment='top', fontweight='bold', color='red')

    # Consumption Points & Indifference Curves
    ax.scatter([c_h, c_f], [w_h, w_f], color=['blue', 'red'], zorder=5, s=80)
    ax.text(c_h, w_h, '  Home consumption in trade', verticalalignment='bottom')
    ax.text(c_f, w_f, '  Foreign Consumption trade', verticalalignment='top')
    
    c_space = np.linspace(0.1, max(max_c_h, max_c_f)*1.5, 100)
    u_h, u_f = (c_h**0.5 * w_h**0.5), (c_f**0.5 * w_f**0.5)
    ax.plot(c_space, (u_h**2)/c_space, 'b:', alpha=0.4)
    ax.plot(c_space, (u_f**2)/c_space, 'r:', alpha=0.4)

limit = max(max_c_h, max_w_h, max_c_f, max_w_f) * 1.2
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)
ax.set_xlabel("Quantity of Cheese")
ax.set_ylabel("Quantity of Wine")
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
st.pyplot(fig)

# --- Analysis Dashboard ---
st.header("Comparative Advantage Analysis")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Home Country")
    st.write(f"Opp. Cost of 1 Cheese: **{oc_c_h:.2f} Wine**")
    if are_costs_equal: st.warning("No Comp. Advantage")
    elif oc_c_h < oc_c_f: st.success("✅ Comp. Advantage: **Cheese**")
    else: st.success("✅ Comp. Advantage: **Wine**")

with col2:
    st.subheader("Foreign Country")
    st.write(f"Opp. Cost of 1 Cheese: **{oc_c_f:.2f} Wine**")
    if are_costs_equal: st.warning("No Comp. Advantage")
    elif oc_c_f < oc_c_h: st.success("✅ Comp. Advantage: **Cheese**")
    else: st.success("✅ Comp. Advantage: **Wine**")

st.divider()

# --- Bottom Message ---
if not use_equilibrium:
    if are_costs_equal:
        st.error("🚫 **No Trade Possible**")
    else:
        lower_bound, upper_bound = min(oc_c_h, oc_c_f), max(oc_c_h, oc_c_f)
        st.info(f"💡 In free trade, the world price of Cheese ($P_C/P_W$) will be between **{lower_bound:.2f}** and **{upper_bound:.2f}** Wine.")
else:
    if are_costs_equal:
        st.error("🚫 **No trade will take place: opportunity costs are the same!**")
    else:
        st.subheader("🌐 Market Clearing Equilibrium")
        st.write("Assuming **Cobb-Douglas Preferences** ($U = C^{0.5}W^{0.5}$), consumers spend 50% of their income on each good.")
        st.info(f"The unique equilibrium world price is **$P_C/P_W = {p_final:.2f}$**.")
        st.write("At this price, both countries maximize utility by specializing production at the points marked on the graph.")
