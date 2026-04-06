import streamlit as st
import numpy as np

# --- 1. FULL DATA TABLES ---

# UPPER RESERVOIR (Target RL: 94.500m | Target MCM: 8.067)
u_rl_table = np.array([
    90.000, 90.025, 90.050, 90.075, 90.100, 90.125, 90.150, 90.175, 90.200, 90.225,
    90.250, 90.275, 90.300, 90.325, 90.350, 90.375, 90.400, 90.425, 90.450, 90.475,
    90.500, 90.525, 90.550, 90.575, 90.600, 90.625, 90.650, 90.675, 90.700, 90.725,
    90.750, 90.775, 90.800, 90.825, 90.850, 90.875, 90.900, 90.925, 90.950, 90.975,
    91.000, 91.125, 91.250, 91.375, 91.500, 91.625, 91.750, 91.875, 92.000, 92.125,
    92.250, 92.375, 92.500, 92.625, 92.750, 92.875, 93.000, 93.100, 93.200, 93.300,
    93.400, 93.500, 93.600, 93.700, 93.800, 93.900, 94.000, 94.100, 94.200, 94.300,
    94.400, 94.425, 94.450, 94.475, 94.500, 95.000
])

u_mcm_table = np.array([
    4.336, 4.354, 4.371, 4.389, 4.406, 4.424, 4.441, 4.459, 4.476, 4.494,
    4.511, 4.599, 4.686, 4.774, 4.861, 4.949, 5.036, 5.124, 5.211, 5.299,
    5.386, 5.474, 5.561, 5.649, 5.736, 5.826, 5.916, 5.997, 6.077, 6.157,
    6.237, 6.318, 6.390, 6.478, 6.539, 6.619, 6.699, 6.779, 6.860, 6.940,
    7.040, 7.141, 7.241, 7.342, 7.448, 7.535, 7.657, 7.759, 7.862, 7.964,
    7.990, 8.016, 8.041, 8.067, 9.081
])

# LOWER RESERVOIR (Safety RL: 90.000m)
l_rl_table = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 90.063, 90.125,
    90.188, 90.250, 90.313, 90.375, 90.438, 90.500, 91.000, 92.000, 93.000, 94.000, 95.000
])

l_mcm_table = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.304, 3.318,
    3.331, 3.345, 3.359, 3.373, 3.386, 3.400, 3.640, 4.020, 4.480, 4.840, 5.940
])

# --- 2. LAYOUT ---
st.set_page_config(page_title="Shift Master Planner", layout="wide")
st.title("📋 Hydro Operations: Multi-Stage Planner")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Phase 1: Upper Reservoir")
    curr_u = st.number_input("Current Upper RL (m)", value=93.400, format="%.3f")
    lake_ph_rate = 0.820 # MCM/MUS
    
    st.divider()
    tunnel_hrs = st.number_input("Tunnel/Gate Open Duration (Hrs)", min_value=0.0, value=1.0)

with col2:
    st.subheader("📍 Phase 2: Lower Reservoir")
    curr_l = st.number_input("Current Lower RL (m)", value=92.000, format="%.3f")
    l_gen_target = st.number_input("Lower PH Planned Gen (MUS)", value=0.120, format="%.3f")
    l_ph_rate = 9.360 # MCM/MUS

# --- 4. CALCULATION ---
if st.button("Calculate Shift Release Target", type="primary"):
    
    if curr_l < 90.000:
        st.error("🚫 Operation Blocked: Lower Reservoir below 90.000m safety limit.")
    else:
        # A. Water to hit 94.50m in Upper Res
        target_u_mcm = 8.067
        idx_u = (np.abs(u_rl_table - curr_u)).argmin()
        start_u_mcm = u_mcm_table[idx_u]
        u_gap = target_u_mcm - start_u_mcm
        
        # B. Water to 'Bank' in Lower Res for their 9.36 rate gen
        lower_demand = l_gen_target * l_ph_rate
        
        # C. Tunnel Flow (Upper to Lower)
        head_diff = curr_u - curr_l
        flow_rate = 0.185 if head_diff >= 3.0 else 0.160
        tunnel_total = flow_rate * tunnel_hrs
        
        # D. Total Water Required from Lake Power House
        total_mcm = u_gap + lower_demand + tunnel_total
        lake_gen_mus = total_mcm / lake_ph_rate
        
        # --- 5. RESULTS ---
        st.divider()
        st.metric("Lake PH Generation Target", f"{lake_gen_mus:.3f} MUS")
        st.success(f"Once Lake PH reaches **{lake_gen_mus:.3f} MUS**, you have released enough water.")
        
        with st.expander("Detailed Handover Data"):
            st.write(f"Upper Res Gap (to 94.50m): **{u_gap:.3f} MCM**")
            st.write(f"Lower PH 'Banked' Water: **{lower_demand:.3f} MCM**")
            st.write(f"Tunnel Flow during Shift: **{tunnel_total:.3f} MCM**")
            st.write("---")
            st.write(f"**Total System Water Requirement: {total_mcm:.3f} MCM**")
