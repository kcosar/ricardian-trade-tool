import streamlit as st
import matplotlib.pyplot as plt

st.title("Interactive Ricardian Trade Model")
st.markdown("Enter the parameters for both countries to see the PPFs and comparative advantages.")

# --- Sidebar Numerical Inputs ---
st.sidebar.header("🏠 Home Country")
L_h = st.sidebar.number_input("Labor Force (L)", min_value=1, value=100)
mpl_c_h = st.sidebar.number_input("MPL Cheese", min_value=0.1, value=4.0, step=0.5)
mpl_w_h = st.sidebar.number_input("MPL Wine", min_value=0.1, value=2.0, step=0.5)

st.sidebar.header("🌍 Foreign Country")
L_f = st.sidebar.number_input("Labor Force (L*)", min_value=1, value=100)
mpl_c_f = st.sidebar.number_input("MPL* Cheese", min_value=0.1, value=1.0, step=0.5)
mpl_w_f = st.sidebar.number_input("MPL* Wine", min_value=0.1, value=5.0, step=0.5)

# --- Logic & Calculations ---
# Intercepts
max_c_h, max_w_h = L_h * mpl_c_h, L_h * mpl_w_h
max_c_f, max_w_f = L_f * mpl_c_f, L_f * mpl_w_f

# Opp Costs (Wine per 1 unit of Cheese)
oc_c_h = mpl_w_h / mpl_c_h
oc_c_f = mpl_w_f / mpl_c_f

# --- Graphing ---
fig, ax = plt.subplots(figsize=(10, 7))

# Plotting the lines
ax.plot([0, max_c_h], [max_w_h, 0], 'b-o', label=f'Home PPF (Slope: -{oc_c_h:.2f})', linewidth=3)
ax.plot([0, max_c_f], [max_w_f, 0], 'r-o', label=f'Foreign PPF (Slope: -{oc_c_f:.2f})', linewidth=3)

# Snapping to axes and adding padding
limit = max(max_c_h, max_w_h, max_c_f, max_w_f) * 1.1
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)

# Aesthetics
ax.set_xlabel("Quantity of Cheese", fontsize=12)
ax.set_ylabel("Quantity of Wine", fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()

st.pyplot(fig)

# --- Analysis Dashboard ---
st.header("Comparative Advantage Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Home Country")
    st.write(f"Opportunity Cost of 1 Cheese: **{oc_c_h:.2f} Wine**")
    if oc_c_h < oc_c_f:
        st.success("✅ Comparative Advantage: **Cheese**")
    else:
        st.info("Advantage: Wine")

with col2:
    st.subheader("Foreign Country")
    st.write(f"Opportunity Cost of 1 Cheese: **{oc_c_f:.2f} Wine**")
    if oc_c_f < oc_c_h:
        st.success("✅ Comparative Advantage: **Cheese**")
    else:
        st.info("Advantage: Wine")

# Terms of Trade logic
st.divider()
lower_bound = min(oc_c_h, oc_c_f)
upper_bound = max(oc_c_h, oc_c_f)
st.info(f"💡 In free trade, the world (relative) price of Cheese ($P_C/P_W$) will be between **{lower_bound:.2f}** and **{upper_bound:.2f}**.")
