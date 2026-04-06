import streamlit as st
import numpy as np

# --- 1. SYNCHRONIZED DATA TABLES ---
u_rl_table = np.array([
    90.000, 90.025, 90.050, 90.075, 90.100, 90.125, 90.150, 90.175, 90.200, 90.225,
    90.250, 90.275, 90.300, 90.325, 90.350, 90.375, 90.400, 90.425, 90.450, 90.475,
    90.500, 90.525, 90.550, 90.575, 90.600, 90.625, 90.650, 90.675, 90.700, 90.725,
    90.750, 90.775, 90.800, 90.825, 90.850, 90.875, 90.900, 90.925, 90.950, 90.975,
    91.000, 92.000, 93.000, 93.400, 94.000, 94.400, 94.425, 94.450, 94.475, 94.500, 95.000
])

u_mcm_table = np.array([
    4.336, 4.354, 4.371, 4.389, 4.406, 4.424, 4.441, 4.459, 4.476, 4.494,
    4.511, 4.529, 4.546, 4.564, 4.581, 4.599, 4.616, 4.634, 4.651, 4.669,
    4.686, 4.704, 4.721, 4.739, 4.756, 4.774, 4.791, 4.809, 4.826, 4.844,
    4.861, 4.879, 4.896, 4.914, 4.931, 4.949, 4.966, 4.984, 5.001, 5.019,
    5.036, 5.736, 6.539, 6.940, 7.535, 7.964, 7.990, 8.016, 8.041, 8.067, 9.081
])

l_rl_table = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 91.000, 92.000, 93.000, 94.000, 95.000
])

l_mcm_table = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.640, 4.020, 4.480, 4.840, 5.940
])

# --- 2. LAYOUT ---
st.set_page_config(page_title="Lake Level & Gate Advisor", layout="wide")
st.title("🌊 Lake Power House: Operations Planner")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Upper Lake Status")
    curr_u = st.number_input("Current Upper RL (m)", value=93.400, format="%.3f")
    lake_ph_rate = 0.820 # MCM/MUS

with col2:
    st.subheader("📍 Lower Reservoir Status")
    curr_l = st.number_input("Current Lower RL (m)", value=92.500, format="%.3f")
    l_gen_target = st.number_input("Lower PH Planned Gen (MUS)", value=0.080, format="%.3f")
    l_ph_rate = 9.360 # MCM/MUS

# --- 4. CALCULATION ---
if st.button("Calculate Total Generation Requirements", type="primary"):
    
    # A. Upper Lake Calculation (Target 94.50m = 8.067 MCM)
    target_u_mcm = 8.067
    idx_u = (np.abs(u_rl_table - curr_u)).argmin()
    start_u_mcm = u_mcm_table[idx_u]
    
    u_gap_mcm = target_u_mcm - start_u_mcm
    gen_for_level = u_gap_mcm / lake_ph_rate
    
    # B. Lower Reservoir Calculation (Safety 90.00m = 3.290 MCM)
    idx_l = (np.abs(l_rl_table - curr_l)).argmin()
    current_l_mcm = l_mcm_table[idx_l]
    min_l_mcm = 3.290
    
    available_l_mcm = current_l_mcm - min_l_mcm
    required_l_mcm = l_gen_target * l_ph_rate
    
    # C. Net Deficit/Transfer Requirement
    net_transfer_needed = max(0.0, required_l_mcm - available_l_mcm)
    gen_for_transfer = net_transfer_needed / lake_ph_rate
    
    # D. Gate Flow Calculation (3-tier)
    head_diff = curr_u - curr_l
    if head_diff > 3.0: flow_rate = 0.17
    elif 2.0 <= head_diff <= 3.0: flow_rate = 0.15
    elif 1.5 <= head_diff < 2.0: flow_rate = 0.12
    else: flow_rate = 0.08
    
    time_to_close = net_transfer_needed / flow_rate if flow_rate > 0 else 0

    # --- 5. RESULTS ---
    st.divider()
    
    # TOTAL TARGET
    total_lake_gen = gen_for_level + gen_for_transfer
    st.header(f"Total Lake PH Gen Target: {total_lake_gen:.3f} MUS")
    
    res1, res2 = st.columns(2)
    
    with res1:
        st.subheader("🏁 Level Goal")
        st.metric("Gen for 94.50m", f"{gen_for_level:.3f} MUS")
        st.write(f"Remaining Volume to fill: **{u_gap_mcm:.3f} MCM**")
        
    with res2:
        st.subheader("🏁 Transfer Goal")
        if net_transfer_needed <= 0:
            st.success("✅ CLOSE GATES: Water is sufficient.")
            st.write(f"Surplus in Lower Res: **{abs(required_l_mcm - available_l_mcm):.3f} MCM**")
        else:
            st.warning(f"🕒 KEEP OPEN for **{time_to_close:.2f} Hours**")
            st.metric("Gen for Transfer", f"{gen_for_transfer:.3f} MUS")

    with st.expander("Detailed Calculation breakdown"):
        st.write(f"Upper Lake starting at **{start_u_mcm:.3f} MCM**.")
        st.write(f"Lower Res has **{available_l_mcm:.3f} MCM** available above 90m.")
        st.write(f"Current Head Difference is **{head_diff:.2f} m**.")
        
