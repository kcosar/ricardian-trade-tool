import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Interactive Ricardian Trade Model")

# --- Sidebar Inputs ---
st.sidebar.header("🏠 Home Country")
L_h = st.sidebar.number_input("Labor Force (L)", min_value=1, value=100)
mpl_c_h = st.sidebar.number_input("MPL Cheese", min_value=0.1, value=4.0, step=0.5)
mpl_w_h = st.sidebar.number_input("MPL Wine", min_value=0.1, value=2.0, step=0.5)

st.sidebar.header("🌍 Foreign Country")
L_f = st.sidebar.number_input("Labor Force (L*)", min_value=1, value=100)
mpl_c_f = st.sidebar.number_input("MPL* Cheese", min_value=0.1, value=1.0, step=0.5)
mpl_w_f = st.sidebar.number_input("MPL* Wine", min_value=0.1, value=5.0, step=0.5)

# --- Utility Selection ---
st.sidebar.divider()
use_utility = st.sidebar.checkbox("Enable Utility Analysis (Cobb-Douglas)")

if use_utility:
    st.sidebar.subheader("Trade Settings")
    # World price must be between the two opp costs
    oc_h = mpl_w_h / mpl_c_h
    oc_f = mpl_w_f / mpl_c_f
    p_min, p_max = sorted([oc_h, oc_f])
    
    # Allow student to pick a world price within the gains-from-trade range
    p_world = st.sidebar.slider("World Price (Pc/Pw)", 
                                 min_value=float(p_min), 
                                 max_value=float(p_max), 
                                 value=float((p_min + p_max)/2))

# --- Logic & Calculations ---
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f
oc_c_h = mpl_w_h / mpl_c_h
oc_c_f = mpl_w_f / mpl_c_f
are_costs_equal = round(oc_c_h, 4) == round(oc_c_f, 4)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot([0, max_c_h], [max_w_h, 0], 'b-', label='Home PPF', linewidth=2, alpha=0.3)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-', label='Foreign PPF', linewidth=2, alpha=0.3)

if use_utility and not are_costs_equal:
    # 1. Determine Specialization and Income
    # Home
    if oc_c_h < oc_c_f: # Home specializes in Cheese
        income_h_w = max_c_h * p_world
        cons_c_h, cons_w_h = (0.5 * income_h_w / p_world), (0.5 * income_h_w)
        ax.plot([0, income_h_w/p_world], [income_h_w, 0], 'b--', label='Home Budget Line')
        ax.scatter(cons_c_h, cons_w_h, color='blue', zorder=5)
    else: # Home specializes in Wine
        income_h_w = max_w_h
        cons_c_h, cons_w_h = (0.5 * income_h_w / p_world), (0.5 * income_h_w)
        ax.plot([0, income_h_w/p_world], [income_h_w, 0], 'b--', label='Home Budget Line')
        ax.scatter(cons_c_h, cons_w_h, color='blue', zorder=5)
        
    # Foreign
    if oc_c_f < oc_c_h: # Foreign specializes in Cheese
        income_f_w = max_c_f * p_world
        cons_c_f, cons_w_f = (0.5 * income_f_w / p_world), (0.5 * income_f_w)
        ax.plot([0, income_f_w/p_world], [income_f_w, 0], 'r--', label='Foreign Budget Line')
        ax.scatter(cons_c_f, cons_w_f, color='red', zorder=5)
    else: # Foreign specializes in Wine
        income_f_w = max_w_f
        cons_c_f, cons_w_f = (0.5 * income_f_w / p_world), (0.5 * income_f_w)
        ax.plot([0, income_f_w/p_world], [income_f_w, 0], 'r--', label='Foreign Budget Line')
        ax.scatter(cons_c_f, cons_w_f, color='red', zorder=5)

    # 2. Draw Indifference Curves (U = C^0.5 * W^0.5)
    c_space = np.linspace(0.1, max(max_c_h, max_c_f)*1.5, 100)
    u_h = (cons_c_h**0.5) * (cons_w_h**0.5)
    u_f = (cons_c_f**0.5) * (cons_w_f**0.5)
    ax.plot(c_space, (u_h**2)/c_space, 'b:', alpha=0.5, label=f'Home Utility: {u_h:.1f}')
    ax.plot(c_space, (u_f**2)/c_space, 'r:', alpha=0.5, label=f'Foreign Utility: {u_f:.1f}')

# Final Graph Styling
limit = max(max_c_h, max_w_h, max_c_f, max_w_f) * 1.3
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)
ax.set_xlabel("Quantity of Cheese")
ax.set_ylabel("Quantity of Wine")
ax.legend()
st.pyplot(fig)

# --- Dashboard Text ---
st.header("Comparative Advantage Analysis")
# ... (Keep your existing columns here) ...

if use_utility and not are_costs_equal:
    st.divider()
    st.subheader("Equilibrium Utilities")
    st.write(f"🏠 **Home Consumption:** {cons_c_h:.1f} Cheese, {cons_w_h:.1f} Wine. Utility: **{u_h:.2f}**")
    st.write(f"🌍 **Foreign Consumption:** {cons_c_f:.1f} Cheese, {cons_w_f:.1f} Wine. Utility: **{u_f:.2f}**")
