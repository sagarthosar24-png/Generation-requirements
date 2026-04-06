import streamlit as st
import numpy as np

# --- 1. DATA TABLES (FULL RL & MCM) ---

# UPPER RESERVOIR (Targeting 94.500 m = 8.067 MCM)
u_rl = np.array([
    90.000, 90.025, 90.050, 90.075, 90.100, 90.125, 90.150, 90.175, 90.200, 90.225,
    90.250, 90.275, 90.300, 90.325, 90.350, 90.375, 90.400, 90.425, 90.450, 90.475,
    90.500, 90.525, 90.550, 90.575, 90.600, 90.625, 90.650, 90.675, 90.700, 90.725,
    90.750, 90.775, 90.800, 90.825, 90.850, 90.875, 90.900, 90.925, 90.950, 90.975,
    91.000, 91.025, 91.050, 91.075, 91.100, 91.125, 91.150, 91.175, 91.200, 91.225,
    91.250, 91.275, 91.300, 91.325, 91.350, 91.375, 91.400, 91.425, 91.450, 91.475,
    91.500, 91.525, 91.550, 91.575, 91.600, 91.625, 91.650, 91.675, 91.700, 91.725,
    91.750, 91.775, 91.800, 91.825, 91.850, 91.875, 91.900, 91.925, 91.950, 91.975,
    92.000, 92.025, 92.050, 92.075, 92.100, 92.125, 92.150, 92.175, 92.200, 92.225,
    92.250, 92.275, 92.300, 92.325, 92.350, 92.375, 92.400, 92.425, 92.450, 92.475,
    92.500, 92.525, 92.550, 92.575, 92.600, 92.625, 92.650, 92.675, 92.700, 92.725,
    92.750, 92.775, 92.800, 92.825, 92.850, 92.875, 92.900, 92.925, 92.950, 92.975,
    93.000, 93.100, 93.200, 93.300, 93.400, 93.500, 93.600, 93.700, 93.800, 93.900,
    94.000, 94.100, 94.200, 94.300, 94.400, 94.425, 94.450, 94.475, 94.500, 95.000
])
u_mcm = np.array([
    4.336, 4.354, 4.371, 4.389, 4.406, 4.424, 4.441, 4.459, 4.476, 4.494,
    4.511, 4.529, 4.546, 4.564, 4.581, 4.599, 4.616, 4.634, 4.651, 4.669,
    4.686, 4.704, 4.721, 4.739, 4.756, 4.774, 4.791, 4.809, 4.826, 4.844,
    4.861, 4.879, 4.896, 4.914, 4.931, 4.949, 4.966, 4.984, 5.001, 5.019,
    5.036, 5.054, 5.071, 5.089, 5.106, 5.124, 5.141, 5.159, 5.176, 5.194,
    5.211, 5.229, 5.246, 5.264, 5.281, 5.299, 5.316, 5.334, 5.351, 5.369,
    5.386, 5.404, 5.421, 5.439, 5.456, 5.474, 5.491, 5.509, 5.526, 5.544,
    5.561, 5.579, 5.596, 5.614, 5.631, 5.649, 5.666, 5.684, 5.701, 5.719,
    5.736, 5.756, 5.776, 5.796, 5.816, 5.836, 5.856, 5.876, 5.896, 5.916,
    5.936, 5.956, 5.976, 5.997, 6.017, 6.037, 6.057, 6.077, 6.097, 6.117,
    6.137, 6.157, 6.177, 6.197, 6.217, 6.237, 6.257, 6.278, 6.298, 6.318,
    6.338, 6.354, 6.370, 6.390, 6.410, 6.434, 6.458, 6.478, 6.498, 6.519,
    6.539, 6.619, 6.699, 6.779, 6.940, 7.040, 7.141, 7.241, 7.342, 7.448,
    7.535, 7.657, 7.759, 7.862, 7.964, 7.990, 8.016, 8.041, 8.067, 9.081
])

# LOWER RESERVOIR (Discharging 9.36 MCM/MUS)
l_rl = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 90.063, 90.125,
    90.188, 90.250, 90.313, 90.375, 90.438, 90.500, 91.000, 92.000, 93.000, 94.000, 95.000
])
l_mcm = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.304, 3.318,
    3.331, 3.345, 3.359, 3.373, 3.386, 3.400, 3.640, 4.020, 4.480, 4.840, 5.940
])

# --- 2. INTERFACE ---
st.set_page_config(page_title="Shift Target Planner", layout="wide")
st.title("⚡ Upper Reservoir 94.50m Planner")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Phase 1: Upper Reservoir")
    curr_u = st.number_input("Current Upper RL (m)", value=93.400, format="%.3f")
    lake_ph_rate = 0.820 # MCM/MUS
    
    st.divider()
    tunnel_on = st.toggle("Tunnel Gate Open?", value=True)
    tunnel_hrs = st.number_input("Tunnel Hours in Shift", min_value=0.0, value=1.0)

with col2:
    st.subheader("📍 Phase 2: Lower Reservoir")
    curr_l = st.number_input("Current Lower RL (m)", value=92.000, format="%.3f")
    l_ph_target = st.number_input("Lower PH Generation Target (MUS)", value=0.120, format="%.3f")
    l_ph_rate = 9.360 # MCM/MUS

# --- 4. CALCULATION ---
if st.button("Calculate Lake Generation Required", type="primary"):
    
    if curr_l < 90.000:
        st.error("🚫 Warning: Lower Reservoir below 90m! Power House Not Operated.")
    else:
        # A. Upper Res Gap (to 94.50m)
        target_mcm = 8.067
        idx_u = (np.abs(u_rl - curr_u)).argmin()
        start_u_mcm = u_mcm[idx_u]
        u_gap = target_mcm - start_u_mcm
        
        # B. Outflow via Tunnel
        tunnel_flow = 0.0
        if tunnel_on:
            diff = curr_u - curr_l
            rate = 0.185 if diff >= 3.0 else 0.160
            tunnel_flow = rate * tunnel_hrs
            
        # C. Outflow via Lower PH
        lower_ph_vol = l_ph_target * l_ph_rate
        
        # D. Total Volume required from Lake PH
        total_vol = u_gap + tunnel_flow + lower_ph_vol
        required_lake_gen = total_vol / lake_ph_rate
        
        # --- 5. RESULTS ---
        st.divider()
        st.metric("Required Lake PH Generation", f"{required_lake_gen:.3f} MUS")
        
        with st.expander("Detailed System Balance"):
            st.write(f"Volume to fill Upper Res: **{u_gap:.3f} MCM**")
            st.write(f"Volume moved to Lower Res (Tunnel): **{tunnel_flow:.3f} MCM**")
            st.write(f"Volume for Lower PH Gen: **{lower_ph_vol:.3f} MCM**")
            st.write(f"---")
            st.write(f"**Total Water Needed from Lake: {total_vol:.3f} MCM**")
            
