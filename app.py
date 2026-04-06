import streamlit as st
import numpy as np

# --- 1. DATA TABLES (Full Resolution) ---
# LAKE RL and Content (Source: 0.82 MCM/MUS)
lake_level_data = np.array([
    90.000, 90.025, 90.050, 90.075, 90.100, 90.125, 90.150, 90.175, 90.200, 90.225,
    90.250, 90.275, 90.300, 90.325, 90.350, 90.375, 90.400, 90.425, 90.450, 90.475,
    90.500, 90.525, 90.550, 90.575, 90.600, 90.625, 90.650, 90.675, 90.700, 90.725,
    90.750, 90.775, 90.800, 90.825, 90.850, 90.875, 90.900, 90.925, 90.950, 90.975,
    91.000, 91.500, 92.000, 92.500, 93.000, 93.400, 94.000, 94.400, 94.450, 94.500, 95.000
])
lake_content_data = np.array([
    4.336, 4.354, 4.371, 4.389, 4.406, 4.424, 4.441, 4.459, 4.476, 4.494,
    4.511, 4.861, 5.211, 5.561, 6.539, 6.940, 7.535, 7.964, 8.016, 8.067, 9.081
])

# LOWER RESERVOIR RL and Content (Source: 9.36 MCM/MUS)
l_level_data = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 90.125, 90.250,
    90.500, 91.000, 91.500, 92.000, 92.500, 93.000, 93.500, 94.000, 94.500, 95.000
])
l_content_data = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.318, 3.345,
    3.400, 3.640, 3.890, 4.020, 4.250, 4.480, 4.660, 4.840, 5.050, 5.940
])

# --- 2. APP LAYOUT ---
st.set_page_config(page_title="3-Stage Hydro Systems", layout="wide")
st.title("🚜 3-Stage Generation Planner")
st.markdown("### Goal: Calculate Lake Generation to hit 94.500 m")

# --- 3. INPUTS ---
st.sidebar.header("Tunnel Configuration")
tunnel_active = st.sidebar.toggle("Tunnel Gate Open?", value=True)
tunnel_time = st.sidebar.number_input("Tunnel Flow Duration (Hrs)", min_value=0.0, value=1.0)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 Phase 1: The Lake")
    c_lake_rl = st.number_input("Current Lake RL (m)", value=93.400, format="%.3f")
    st.caption("Discharge Rate: 0.82 MCM/MUS")

with col2:
    st.subheader("📍 Phase 2: Upper Res")
    c_upper_rl = st.number_input("Upper Res RL (m)", value=92.500, format="%.3f")

with col3:
    st.subheader("📍 Phase 3: Lower Res")
    c_lower_rl = st.number_input("Lower Res RL (m)", value=92.000, format="%.3f")
    l_ph_target = st.number_input("Lower PH Target (MUS)", value=0.120, format="%.3f")
    st.caption("Discharge Rate: 9.36 MCM/MUS")

# --- 4. CALCULATION ---
if st.button("Generate Detailed Plan", type="primary"):
    
    if c_lower_rl < 90.0:
        st.error("🚫 Operation Blocked: Lower Reservoir is below 90.000m safety limit.")
    else:
        # A. Lake Volume Gap (Target 94.50m = 8.067 MCM)
        target_mcm = 8.067
        idx_lake = (np.abs(lake_level_data - c_lake_rl)).argmin()
        lake_start_mcm = lake_content_data[idx_lake]
        lake_gap = target_mcm - lake_start_mcm
        
        # B. Lower PH Water Demand (9.36 Rate)
        lower_demand = l_ph_target * 9.360
        
        # C. Tunnel Flow (Upper to Lower)
        tunnel_mcm = 0.0
        if tunnel_active:
            diff = c_upper_rl - c_lower_rl
            rate = 0.185 if diff >= 3.0 else 0.160
            tunnel_mcm = rate * tunnel_time
            
        # D. Total Required from Lake
        total_mcm = lake_gap + lower_demand + tunnel_mcm
        required_lake_gen = total_mcm / 0.820
        
        # --- 5. OUTPUTS ---
        st.divider()
        st.metric("Required Lake Power House Generation", f"{required_lake_gen:.3f} MUS")
        
        with st.expander("Water Balance Breakdown"):
            st.write(f"Lake Gap to 94.50m: **{lake_gap:.3f} MCM**")
            st.write(f"Lower PH Need (at 9.36): **{lower_demand:.3f} MCM**")
            if tunnel_active:
                st.write(f"Tunnel Flow Addition: **{tunnel_mcm:.3f} MCM**")
            st.write("---")
            st.write(f"**Total Water Balance: {total_mcm:.3f} MCM**")
            
