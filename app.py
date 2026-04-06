import streamlit as st
import numpy as np

# --- 1. FULL DATA TABLES ---
# Upper Lake Level (RL) and Content (MCM)
u_level_data = np.array([
    90.000, 90.100, 90.200, 90.300, 90.400, 90.500, 90.600, 90.700, 90.800, 90.900,
    91.000, 91.100, 91.200, 91.300, 91.400, 91.500, 91.600, 91.700, 91.800, 91.900,
    92.000, 92.100, 92.200, 92.300, 92.400, 92.500, 92.600, 92.700, 92.800, 92.900,
    93.000, 93.100, 93.200, 93.300, 93.400, 93.500, 93.600, 93.700, 93.800, 93.900,
    94.000, 94.100, 94.200, 94.300, 94.400, 94.425, 94.450, 94.475, 94.500, 95.000
])
u_content_data = np.array([
    4.336, 4.406, 4.476, 4.546, 4.616, 4.686, 4.756, 4.826, 4.896, 4.966,
    5.036, 5.106, 5.176, 5.246, 5.316, 5.386, 5.456, 5.526, 5.596, 5.666,
    5.736, 5.816, 5.896, 5.976, 6.057, 6.137, 6.217, 6.298, 6.370, 6.458,
    6.539, 6.619, 6.699, 6.779, 6.940, 7.040, 7.141, 7.241, 7.342, 7.448,
    7.535, 7.657, 7.759, 7.862, 7.964, 7.990, 8.016, 8.041, 8.067, 9.081
])

# Lower Reservoir Level (RL) and Content (MCM)
l_level_data = np.array([
    89.000, 89.250, 89.500, 89.750, 90.000, 90.250, 90.500, 90.750, 91.000, 91.250,
    91.500, 91.750, 92.000, 92.250, 92.500, 92.750, 93.000, 93.250, 93.500, 93.750,
    94.000, 94.250, 94.500, 94.750, 95.000
])
l_content_data = np.array([
    2.870, 2.975, 3.080, 3.185, 3.290, 3.345, 3.400, 3.520, 3.640, 3.765,
    3.890, 3.955, 4.020, 4.135, 4.250, 4.365, 4.480, 4.570, 4.660, 4.750,
    4.840, 4.945, 5.050, 5.273, 5.940
])

# --- 2. LAYOUT ---
st.set_page_config(page_title="Hydro Ops & Planner", layout="centered")
st.title("⚡ Reservoir Management System")

# --- 3. INPUTS ---
st.header("1. Current Status")
col1, col2 = st.columns(2)
with col1:
    curr_u_lvl = st.number_input("Current Upper Lake RL (m)", value=93.400, format="%.3f")
with col2:
    curr_l_lvl = st.number_input("Current Lower Res. RL (m)", value=92.000, format="%.3f")
    if curr_l_lvl < 90.0:
        st.warning("⚠️ Lower Reservoir below 90m: Generation Restricted.")

st.header("2. Operation Targets")
col3, col4 = st.columns(2)
with col3:
    l_gen_target = st.number_input("Lower PH Gen Target (MUS)", value=0.120, format="%.3f")
with col4:
    u_water_rate = st.number_input("Upper Water Rate (MCM/MUS)", value=0.820, format="%.3f")

# THE TOGGLE & GATE LOGIC
st.divider()
gate_active = st.toggle("Open Interconnecting Gate?", value=True)
if gate_active:
    gate_hours = st.number_input("Duration Gate is Open (Hrs)", min_value=0.0, value=1.0, step=0.5)
else:
    st.info("Gate is Closed: No water flow between reservoirs.")

# --- 4. CALCULATION ---
if st.button("Calculate Required Upper PH Generation", type="primary"):
    
    # A. Volume Gap for Upper Lake (Target 94.50m)
    target_mcm = 8.067
    idx_u = (np.abs(u_level_data - curr_u_lvl)).argmin()
    start_u_mcm = u_content_data[idx_u]
    volume_to_fill = target_mcm - start_u_mcm
    
    # B. Lower Reservoir Demand
    # Water needed for target generation
    lower_ph_demand = l_gen_target * 9.360
    
    # C. Gate Discharge (If toggle is ON)
    gate_discharge = 0.0
    if gate_active:
        head_diff = curr_u_lvl - curr_l_lvl
        # Operational flow rate logic
        flow_rate = 0.185 if head_diff >= 3.0 else 0.160
        gate_discharge = flow_rate * gate_hours
    
    # D. Total Water Required from Upper Lake
    # It must cover the filling of the lake PLUS whatever is released/leaked
    total_mcm_needed = volume_to_fill + lower_ph_demand + gate_discharge
    
    # E. Convert to MUS
    req_gen_mus = total_mcm_needed / u_rate

    # --- 5. RESULTS ---
    st.divider()
    if req_gen_mus < 0:
        st.success(f"Lake is already above target. Surplus: {abs(total_mcm_needed):.3f} MCM")
    else:
        st.metric("Required Upper PH Generation", f"{req_gen_mus:.3f} MUS")
        
    with st.expander("Detailed Calculation Log"):
        st.write(f"Volume to reach 94.50m: **{volume_to_fill:.3f} MCM**")
        st.write(f"Lower PH Target Demand: **{lower_ph_demand:.3f} MCM**")
        if gate_active:
            st.write(f"Gate Release/Loss: **{gate_discharge:.3f} MCM**")
        st.write(f"---")
        st.write(f"**Total Water to be Processed: {total_mcm_needed:.3f} MCM**")
