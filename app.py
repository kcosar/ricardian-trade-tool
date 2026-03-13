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
# Max outputs for PPF intercepts
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

# Opportunity Costs (Wine in terms of Cheese)
opp_cost_h = mpl_c_h / mpl_w_h
opp_cost_f = mpl_c_f / mpl_w_f

# World Price (Simplified: Midpoint between the two opportunity costs)
p_world = (opp_cost_h + opp_cost_f) / 2

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 6))

# Home PPF
ax.plot([0, max_c_h], [max_w_h, 0], 'b-', label='Home PPF', linewidth=2)
# Foreign PPF
ax.plot([0, max_c_f], [max_w_f, 0], 'r-', label='Foreign PPF', linewidth=2)

# Budget Line (Trade Line) example for Home
# If Home specializes in Cheese (assuming opp_cost_h < opp_cost_f)
if opp_cost_h < opp_cost_f:
    # Home specializes in Cheese
    ax.plot([0, max_c_h], [max_c_h * p_world, 0], 'b--', alpha=0.5, label='Home Consumption Possibilities')
else:
    # Home specializes in Wine
    ax.plot([0, max_w_h / p_world], [max_w_h, 0], 'b--', alpha=0.5, label='Home Consumption Possibilities')

ax.set_xlabel("Quantity of Cheese")
ax.set_ylabel("Quantity of Wine")
ax.legend()
st.pyplot(fig)

# --- Display Comparative Advantage ---
st.write(f"**Home Opportunity Cost of Cheese:** {opp_cost_h:.2f} Wine")
st.write(f"**Foreign Opportunity Cost of Cheese:** {opp_cost_f:.2f} Wine")

if opp_cost_h < opp_cost_f:
    st.success("Home has a Comparative Advantage in Cheese!")
else:
    st.success("Foreign has a Comparative Advantage in Cheese!")