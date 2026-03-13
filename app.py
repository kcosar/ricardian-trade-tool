import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Interactive Ricardian Trade Model")

# --- Sidebar Inputs ---
st.sidebar.header("Home Country Parameters")
L_h = st.sidebar.slider("Labor (Home)", 100, 1000, 400)
mpl_c_h = st.sidebar.slider("MPL Cheese (Home)", 1, 10, 4)
mpl_w_h = st.sidebar.slider("MPL Wine (Home)", 1, 10, 2)

st.sidebar.header("Foreign Country Parameters")
L_f = st.sidebar.slider("Labor (Foreign)", 100, 1000, 400)
mpl_c_f = st.sidebar.slider("MPL Cheese (Foreign)", 1, 10, 1)
mpl_w_f = st.sidebar.slider("MPL Wine (Foreign)", 1, 10, 5)

# --- Calculations ---
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 6))

# Home PPF (Blue)
ax.plot([0, max_c_h], [max_w_h, 0], 'b-o', label='Home PPF', linewidth=3)

# Foreign PPF (Red)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-o', label='Foreign PPF', linewidth=3)

# --- The "Snap" Fix ---
# We find the largest value across both axes to keep the scale consistent
max_val = max(max_c_h, max_w_h, max_c_f, max_w_f) * 1.1

ax.set_xlim(0, max_val)
ax.set_ylim(0, max_val)

# Add styling
ax.set_xlabel("Quantity of Cheese", fontsize=12)
ax.set_ylabel("Quantity of Wine", fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()

st.pyplot(fig)

# --- Display Comparative Advantage Logic ---
opp_cost_c_h = mpl_w_h / mpl_c_h
opp_cost_c_f = mpl_w_f / mpl_c_f

st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.metric("Home Opp. Cost (Cheese)", f"{opp_cost_c_h:.2f} Wine")
with col2:
    st.metric("Foreign Opp. Cost (Cheese)", f"{opp_cost_c_f:.2f} Wine")
