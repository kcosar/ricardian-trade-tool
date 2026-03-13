import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Interactive Ricardian Trade Model")

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
use_utility = st.sidebar.checkbox("Enable Equilibrium Analysis")

# --- Logic & Calculations ---
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

oc_c_h = mpl_w_h / mpl_c_h
oc_c_f = mpl_w_f / mpl_c_f
are_costs_equal = round(oc_c_h, 4) == round(oc_c_f, 4)

# Calculate Equilibrium World Price (Market Clearing)
# With 0.5/0.5 weights, World Demand is Pc/Pw = World Wine / World Cheese
if not are_costs_equal:
    # Assuming complete specialization for the initial equilibrium check
    if oc_c_h < oc_c_f: # Home exports Cheese, Foreign exports Wine
        world_c_supply = max_c_h
        world_w_supply = max_w_f
    else: # Foreign exports Cheese, Home exports Wine
        world_c_supply = max_c_f
        world_w_supply = max_w_h
    
    p_world = world_w_supply / world_c_supply
    
    # Check if p_world is within the bounds. If not, price hits a country's OC
    lower_b, upper_b = sorted([oc_c_h, oc_c_f])
    p_world = max(lower_b, min(p_world, upper_b))
else:
    p_world = oc_c_h

# --- Graphing ---
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot([0, max_c_h], [max_w_h, 0], 'b-', label='Home PPF', linewidth=3)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-', label='Foreign PPF', linewidth=3)

if use_utility and not are_costs_equal:
    # Home Budget & Consumption
    inc_h = max_c_h * p_world if oc_c_h < oc_c_f else max_w_h
    c_h, w_h = (0.5 * inc_h / p_world), (0.5 * inc_h)
    ax.plot([0, inc_h/p_world], [inc_h, 0], 'b--', alpha=0.6, label='Home Budget Line')
    
    # Foreign Budget & Consumption
    inc_f = max_c_f * p_world if oc_c_f < oc_c_h else max_w_f
    c_f, w_f = (0.5 * inc_f / p_world), (0.5 * inc_f)
    ax.plot([0, inc_f/p_world], [inc_f, 0], 'r--', alpha=0.6, label='Foreign Budget Line')

    # Indifference Curves
    ax.scatter([c_h, c_f], [w_h, w_f], color=['blue', 'red'], zorder=5)
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

# --- Market Equilibrium Results ---
if are_costs_equal:
    st.error("🚫 **No Trade Possible**")
else:
    st.subheader("🌐 Market Clearing Equilibrium")
    st.info(f"The equilibrium world relative price of Cheese ($P_C/P_W$) is **{p_world:.2f}**.")
    st.write(f"At this price, world supply of both goods matches world demand based on Cobb-Douglas preferences.")
    
    if use_utility:
        st.write(f"🏠 **Home consumes:** {c_h:.1f} Cheese, {w_h:.1f} Wine")
        st.write(f"🌍 **Foreign consumes:** {c_f:.1f} Cheese, {w_f:.1f} Wine")
