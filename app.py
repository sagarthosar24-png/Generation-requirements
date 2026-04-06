import streamlit as st
import numpy as np

# --- 1. SYNCHRONIZED DATA TABLES ---

# UPPER RESERVOIR (0.025m increments aligned with MCM)
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

# LOWER RESERVOIR
l_rl_table = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 91.000, 92.000, 93.000, 94.000, 95.000
])

l_mcm_table = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.640, 4.020, 4.480, 4.840, 5.940
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
    
    # SAFETY CHECK: Ensure tables are same length
    if len(u_rl_table) != len(u_mcm_table):
        st.error(f"Table Error: Upper RL has {len(u_rl_table)} items, but MCM has {len(u_mcm_table)}.")
    elif curr_l < 90.000:
        st.error("🚫 Operation Blocked: Lower Reservoir below 90.000m safety limit.")
    else:
        # A. Water to hit 94.50m in Upper Res
        target_u_mcm = 8.067
        idx_u = (np.abs(u_rl_table - curr_u)).argmin()
        start_u_mcm = u_mcm_table[idx_u]
        u_gap = target_u_mcm - start_u_mcm
        
        # B. Water for Lower Res target
        lower_demand = l_gen_target * l_ph_rate
        
        # C. Tunnel Flow
        head_diff = curr_u - curr_l
        flow_rate = 0.185 if head_diff >= 3.0 else 0.160
        tunnel_total = flow_rate * tunnel_hrs
        
        # D. Final Calculation
        total_mcm = u_gap + lower_demand + tunnel_total
        lake_gen_mus = total_mcm / lake_ph_rate
        
        # --- 5. RESULTS ---
        st.divider()
        st.metric("Lake PH Generation Target", f"{lake_gen_mus:.3f} MUS")
        st.success(f"Once Lake PH reaches **{lake_gen_mus:.3f} MUS**, targets are met.")
        
        with st.expander("Detailed Handover Data"):
            st.write(f"Upper Res RL Lookup: **{u_rl_table[idx_u]:.3f} m**")
            st.write(f"Upper Res Gap: **{u_gap:.3f} MCM**")
            st.write(f"Lower PH Demand: **{lower_demand:.3f} MCM**")
            st.write(f"Tunnel Flow: **{tunnel_total:.3f} MCM**")
