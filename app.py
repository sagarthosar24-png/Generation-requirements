import streamlit as st
import numpy as np

# --- 1. FULL DATA TABLES ---

# Upper Lake Level (RL) and Content (MCM)
u_level_data = np.array([
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
    93.000, 93.025, 93.050, 93.075, 93.100, 93.125, 93.150, 93.175, 93.200, 93.225,
    93.250, 93.275, 93.300, 93.325, 93.350, 93.375, 93.400, 93.425, 93.450, 93.475,
    93.500, 93.525, 93.550, 93.575, 93.600, 93.625, 93.650, 93.675, 93.700, 93.725,
    93.750, 93.775, 93.800, 93.825, 93.850, 93.875, 93.900, 93.925, 93.950, 93.975,
    94.000, 94.025, 94.050, 94.075, 94.100, 94.125, 94.150, 94.175, 94.200, 94.225,
    94.250, 94.275, 94.300, 94.325, 94.350, 94.375, 94.400, 94.425, 94.450, 94.475,
    94.500, 94.525, 94.550, 94.575, 94.600, 94.625, 94.650, 94.675, 94.700, 94.725,
    94.750, 94.775, 94.800, 94.825, 94.850, 94.875, 94.900, 94.925, 94.950, 94.975,
    95.000
])

u_content_data = np.array([
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
    6.539, 6.559, 6.579, 6.599, 6.619, 6.639, 6.659, 6.679, 6.699, 6.719,
    6.739, 6.759, 6.779, 6.800, 6.820, 6.840, 6.860, 6.880, 6.900, 6.920,
    6.940, 6.960, 6.980, 7.000, 7.020, 7.040, 7.060, 7.081, 7.101, 7.121,
    7.141, 7.161, 7.181, 7.201, 7.221, 7.241, 7.261, 7.281, 7.301, 7.322,
    7.342, 7.368, 7.394, 7.411, 7.427, 7.448, 7.469, 7.491, 7.512, 7.524,
    7.535, 7.596, 7.657, 7.708, 7.759, 7.811, 7.862, 7.913, 7.964, 8.016,
    8.067, 8.118, 8.169, 8.220, 8.271, 8.323, 8.374, 8.425, 8.476, 8.528,
    8.579, 8.630, 8.681, 8.733, 8.785, 8.836, 8.886, 8.937, 8.988, 9.035,
    9.081
])

# Lower Reservoir Level (RL) and Content (MCM)
l_level_data = np.array([
    89.000, 89.125, 89.250, 89.375, 89.500, 89.625, 89.750, 90.000, 90.063, 90.125, 
    90.188, 90.250, 90.313, 90.375, 90.438, 90.500, 90.563, 90.625, 90.688, 90.750, 
    90.813, 90.875, 90.938, 91.000, 91.063, 91.125, 91.188, 91.250, 91.313, 91.375, 
    91.438, 91.500, 91.563, 91.625, 91.688, 91.750, 91.813, 91.875, 91.938, 92.000, 
    92.063, 92.125, 92.188, 92.250, 92.313, 92.375, 92.438, 92.500, 92.563, 92.625, 
    92.688, 92.750, 92.813, 92.875, 92.938, 93.000, 93.063, 93.125, 93.188, 93.250, 
    93.313, 93.375, 93.438, 93.500, 93.563, 93.625, 93.688, 93.750, 93.813, 93.875, 
    93.938, 94.000, 94.063, 94.125, 94.188, 94.250, 94.313, 94.375, 94.438, 94.500, 
    94.563, 94.625, 94.688, 94.750, 94.813, 94.875, 94.938, 95.000
])

l_content_data = np.array([
    2.870, 2.923, 2.975, 3.028, 3.080, 3.133, 3.185, 3.290, 3.304, 3.318, 
    3.331, 3.345, 3.359, 3.373, 3.386, 3.400, 3.430, 3.460, 3.490, 3.520, 
    3.550, 3.580, 3.610, 3.640, 3.671, 3.703, 3.734, 3.765, 3.796, 3.828, 
    3.859, 3.890, 3.906, 3.923, 3.939, 3.955, 3.971, 3.988, 4.004, 4.020, 
    4.049, 4.078, 4.106, 4.135, 4.164, 4.193, 4.221, 4.250, 4.279, 4.308, 
    4.336, 4.365, 4.394, 4.423, 4.451, 4.480, 4.503, 4.525, 4.548, 4.570, 
    4.593, 4.615, 4.638, 4.660, 4.683, 4.705, 4.728, 4.750, 4.773, 4.795, 
    4.818, 4.840, 4.866, 4.893, 4.919, 4.945, 4.971, 4.998, 5.024, 5.050, 
    5.161, 5.273, 5.384, 5.495, 5.606, 5.718, 5.829, 5.940
])

# --- 2. INTERFACE SETUP ---
st.set_page_config(page_title="Integrated Power Ops", layout="wide")
st.title("🌊 Hydro Plant Integrated Calculator")

# Sidebar for Navigation
calc_mode = st.sidebar.radio("Select Calculator Mode", ["End-of-Shift Prediction", "Generation Target Planner"])

# --- 3. MODE 1: END-OF-SHIFT PREDICTION ---
if calc_mode == "End-of-Shift Prediction":
    st.header("预测湖水位 (Prediction)")
    with st.sidebar:
        st.header("Gate Configuration")
        gate_open = st.toggle("Interconnecting Gate Open?", value=False)
        gate_hours = st.number_input("Hours Open during Shift", min_value=0.0, value=1.0, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        u_lvl = st.number_input("Upper Lake Level (m)", value=94.400, format="%.3f")
        gen_mus = st.number_input("Upper PH Generation (MUS)", value=0.120, format="%.3f")
    with col2:
        l_lvl = st.number_input("Lower Res. Level (m)", value=90.000, format="%.3f")

    if st.button("Calculate Result", type="primary"):
        idx_u = (np.abs(u_level_data - u_lvl)).argmin()
        initial_mcm = u_content_data[idx_u]
        gen_vol = gen_mus * 0.820
        
        gate_mcm = 0.0
        if gate_open:
            diff = u_lvl - l_lvl
            rate = 0.185 if diff >= 3.0 else 0.160
            gate_mcm = rate * gate_hours
            
        final_mcm = initial_mcm + gen_vol - gate_mcm
        
        if final_mcm > 9.081: final_rl = 95.000
        else:
            idx_f = (np.abs(u_content_data - final_mcm)).argmin()
            final_rl = u_level_data[idx_f]
            
        st.divider()
        st.metric("Final Upper Lake Level", f"{final_rl:.3f} m")
        st.info(f"Total Content: {final_mcm:.3f} MCM")

# --- 4. MODE 2: TARGET PLANNER ---
else:
    st.header("🎯 Generation Target Planner")
    st.markdown("Calculate generation needed to reach **94.500 m (8.067 MCM)**.")
    
    col1, col2 = st.columns(2)
    with col1:
        u_lvl_now = st.number_input("Current Upper Lake Level (m)", value=94.400, format="%.3f")
        u_rate = st.number_input("Upper PH Water Rate (MCM/MUS)", value=0.820, format="%.3f")
    with col2:
        l_gen_target = st.number_input("Lower PH Gen Target (MUS)", value=0.000, format="%.3f")
        l_rate = st.number_input("Lower PH Water Rate (MCM/MUS)", value=9.360, format="%.3f")

    if st.button("Calculate Required Generation", type="primary"):
        # Target Content at 94.50
        target_mcm = 8.067
        
        # Current Content
        idx_now = (np.abs(u_level_data - u_lvl_now)).argmin()
        current_mcm = u_content_data[idx_now]
        
        # Water demand for lower PH
        lower_demand = l_gen_target * l_rate
        
        # Total MCM needed from Lake
        volume_gap = target_mcm - current_mcm
        total_needed = volume_gap + lower_demand
        
        # Required Gen at Upper PH
        req_gen = total_needed / u_rate
        
        st.divider()
        if req_gen < 0:
            st.success(f"Lake level is already above target. Surplus: {abs(total_needed):.3f} MCM")
        else:
            st.metric("Required Upper PH Generation", f"{req_gen:.3f} MUS")
            st.write(f"This uses **{total_needed:.3f} MCM** total water.")
