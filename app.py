import streamlit as st
import numpy as np

# --- 1. DATA TABLES ---
u_data = {
    90.000: 4.336, 90.025: 4.354, 90.050: 4.371, 90.075: 4.389, 90.100: 4.406,
    90.125: 4.424, 90.150: 4.441, 90.175: 4.459, 90.200: 4.476, 90.225: 4.494,
    90.250: 4.511, 90.275: 4.529, 90.300: 4.546, 90.325: 4.564, 90.350: 4.581,
    90.375: 4.599, 90.400: 4.616, 90.425: 4.634, 90.450: 4.651, 90.475: 4.669,
    90.500: 4.686, 90.525: 4.704, 90.550: 4.721, 90.575: 4.739, 90.600: 4.756,
    90.625: 4.774, 90.650: 4.791, 90.675: 4.809, 90.700: 4.826, 90.725: 4.844,
    90.750: 4.861, 90.775: 4.879, 90.800: 4.896, 90.825: 4.914, 90.850: 4.931,
    90.875: 4.949, 90.900: 4.966, 90.925: 4.984, 90.950: 5.001, 90.975: 5.019,
    91.000: 5.036, 91.025: 5.054, 91.050: 5.071, 91.075: 5.089, 91.100: 5.106,
    91.125: 5.124, 91.150: 5.141, 91.175: 5.159, 91.200: 5.176, 91.225: 5.194,
    91.250: 5.211, 91.275: 5.229, 91.300: 5.246, 91.325: 5.264, 91.350: 5.281,
    91.375: 5.299, 91.400: 5.316, 91.425: 5.334, 91.450: 5.351, 91.475: 5.369,
    91.500: 5.386, 91.525: 5.404, 91.550: 5.421, 91.575: 5.439, 91.600: 5.456,
    91.625: 5.474, 91.650: 5.491, 91.675: 5.509, 91.700: 5.526, 91.725: 5.544,
    91.750: 5.561, 91.775: 5.579, 91.800: 5.596, 91.825: 5.614, 91.850: 5.631,
    91.875: 5.649, 91.900: 5.666, 91.925: 5.684, 91.950: 5.701, 91.975: 5.719,
    92.000: 5.736, 92.025: 5.756, 92.050: 5.776, 92.075: 5.796, 92.100: 5.816,
    92.125: 5.836, 92.150: 5.856, 92.175: 5.876, 92.200: 5.896, 92.225: 5.916,
    92.250: 5.936, 92.275: 5.956, 92.300: 5.976, 92.325: 5.997, 92.350: 6.017,
    92.375: 6.037, 92.400: 6.057, 92.425: 6.077, 92.450: 6.097, 92.475: 6.117,
    92.500: 6.137, 92.525: 6.157, 92.550: 6.177, 92.575: 6.197, 92.600: 6.217,
    92.625: 6.237, 92.650: 6.257, 92.675: 6.278, 92.700: 6.298, 92.725: 6.318,
    92.750: 6.338, 92.775: 6.354, 92.800: 6.370, 92.825: 6.390, 92.850: 6.410,
    92.875: 6.434, 92.900: 6.458, 92.925: 6.478, 92.950: 6.498, 92.975: 6.519,
    93.000: 6.539, 93.025: 6.559, 93.050: 6.579, 93.075: 6.599, 93.100: 6.619,
    93.125: 6.639, 93.150: 6.659, 93.175: 6.679, 93.200: 6.699, 93.225: 6.719,
    93.250: 6.739, 93.275: 6.759, 93.300: 6.779, 93.325: 6.800, 93.350: 6.820,
    93.375: 6.840, 93.400: 6.860, 93.425: 6.880, 93.450: 6.900, 93.475: 6.920,
    93.500: 6.940, 93.525: 6.960, 93.550: 6.980, 93.575: 7.000, 93.600: 7.020,
    93.625: 7.040, 93.650: 7.060, 93.675: 7.081, 93.700: 7.101, 93.725: 7.121,
    93.750: 7.141, 93.775: 7.161, 93.800: 7.181, 93.825: 7.201, 93.850: 7.221,
    93.875: 7.241, 93.900: 7.261, 93.925: 7.281, 93.950: 7.301, 93.975: 7.322,
    94.000: 7.342, 94.025: 7.368, 94.050: 7.394, 94.075: 7.411, 94.100: 7.427,
    94.125: 7.448, 94.150: 7.469, 94.175: 7.491, 94.200: 7.512, 94.225: 7.524,
    94.250: 7.535, 94.275: 7.596, 94.300: 7.657, 94.325: 7.708, 94.350: 7.759,
    94.375: 7.811, 94.400: 7.862, 94.425: 7.913, 94.450: 7.964, 94.475: 8.016,
    94.500: 8.067, 94.525: 8.118, 94.550: 8.169, 94.575: 8.220, 94.600: 8.271,
    94.625: 8.323, 94.650: 8.374, 94.675: 8.425, 94.700: 8.476, 94.725: 8.528,
    94.750: 8.579, 94.775: 8.630, 94.800: 8.681, 94.825: 8.733, 94.850: 8.785,
    94.875: 8.836, 94.900: 8.886, 94.925: 8.937, 94.950: 8.988, 94.975: 9.035,
    95.000: 9.081
}

l_data = {
    89.000: 2.870, 89.125: 2.923, 89.250: 2.975, 89.375: 3.028, 89.500: 3.080,
    89.625: 3.133, 89.750: 3.185, 90.000: 3.290, 90.063: 3.304, 90.125: 3.318,
    90.188: 3.331, 90.250: 3.345, 90.313: 3.359, 90.375: 3.373, 90.438: 3.386,
    90.500: 3.400, 90.563: 3.430, 90.625: 3.460, 90.688: 3.490, 90.750: 3.520,
    90.813: 3.550, 90.875: 3.580, 90.938: 3.610, 91.000: 3.640, 91.063: 3.671,
    91.125: 3.703, 91.188: 3.734, 91.250: 3.765, 91.313: 3.796, 91.375: 3.828,
    91.438: 3.859, 91.500: 3.890, 91.563: 3.906, 91.625: 3.923, 91.688: 3.939,
    91.750: 3.955, 91.813: 3.971, 91.875: 3.988, 91.938: 4.004, 92.000: 4.020,
    92.063: 4.049, 92.125: 4.078, 92.188: 4.106, 92.250: 4.135, 92.313: 4.164,
    92.375: 4.193, 92.438: 4.221, 92.500: 4.250, 92.563: 4.279, 92.625: 4.308,
    92.688: 4.336, 92.750: 4.365, 92.813: 4.394, 92.875: 4.423, 92.938: 4.451,
    93.000: 4.480, 93.063: 4.503, 93.125: 4.525, 93.188: 4.548, 93.250: 4.570,
    93.313: 4.593, 93.375: 4.615, 93.438: 4.638, 93.500: 4.660, 93.563: 4.683,
    93.625: 4.705, 93.688: 4.728, 93.750: 4.750, 93.813: 4.773, 93.875: 4.795,
    93.938: 4.818, 94.000: 4.840, 94.063: 4.866, 94.125: 4.893, 94.188: 4.919,
    94.250: 4.945, 94.313: 4.971, 94.375: 4.998, 94.438: 5.024, 94.500: 5.050,
    94.563: 5.161, 94.625: 5.273, 94.688: 5.384, 94.750: 5.495, 94.813: 5.606,
    94.875: 5.718, 94.938: 5.829, 95.000: 5.940
}

# --- 2. LAYOUT ---
st.set_page_config(page_title="BTRP-Rewalje Dispatch Planner", layout="wide")
st.title("⚡ Operational Shift Planner")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 BTRP DAM (Upper Lake)")
    curr_u = st.number_input("Current Level (m)", value=94.400, format="%.3f", step=0.025)
    u_rate = 0.820  # MCM/MUS (BTRP Gen Rate)

with col2:
    st.subheader("📍 Rewalje Forebay (Lower Reservoir)")
    curr_l = st.number_input("Current Level (m) ", value=92.700, format="%.3f", step=0.063)
    l_gen_req = st.number_input("Planned Rewalje PH Gen (mus)", value=0.280, format="%.3f")
    l_conversion = 9.360 # MCM/MUS for Rewalje PH

# --- 4. CALCULATION ---
if st.button("Generate Dispatch Report", type="primary"):
    
    # Static Reference for Rewalje Floor
    L_FLOOR_MCM = 3.290  # Storage at 90.000m
    
    # 1. Fetch Current Volumes
    u_rl_list = np.array(list(u_data.keys()))
    u_idx = (np.abs(u_rl_list - curr_u)).argmin()
    start_u_mcm = u_data[u_rl_list[u_idx]]
    
    l_rl_list = np.array(list(l_data.keys()))
    l_idx = (np.abs(l_rl_list - curr_l)).argmin()
    start_l_mcm = l_data[l_rl_list[l_idx]]

    # 2. REQUIRED TRANSFER (Your Logic)
    # Total water needed for Rewalje gen minus the current buffer above 90.000m
    total_needed_l_mcm = l_gen_req * l_conversion
    available_buffer_l = start_l_mcm - L_FLOOR_MCM
    
    transfer_needed_mcm = max(0.0, total_needed_l_mcm - available_buffer_l)
    
    # 3. Iterative Gate Loop
    sim_u_mcm = start_u_mcm
    sim_l_mcm = start_l_mcm
    total_mcm_moved = 0.0
    minutes_elapsed = 0
    rates_used = []
    
    if transfer_needed_mcm > 0:
        while total_mcm_moved < transfer_needed_mcm:
            # Find closest RLs based on current simulated volume
            u_vals = np.array(list(u_data.values()))
            l_vals = np.array(list(l_data.values()))
            
            curr_sim_u_rl = u_rl_list[(np.abs(u_vals - sim_u_mcm)).argmin()]
            curr_sim_l_rl = l_rl_list[(np.abs(l_vals - sim_l_mcm)).argmin()]
            
            head_diff = curr_sim_u_rl - curr_sim_l_rl
            
            # Flow rates based on head
            if head_diff > 3.0: flow = 0.17
            elif 2.0 <= head_diff <= 3.0: flow = 0.15
            elif 1.5 <= head_diff < 2.0: flow = 0.12
            elif head_diff > 0: flow = 0.08
            else: flow = 0.00
            
            rates_used.append(flow)
            step_mcm = flow * (5 / 60) # 5 min step
            sim_u_mcm -= step_mcm
            sim_l_mcm += step_mcm
            total_mcm_moved += step_mcm
            minutes_elapsed += 5
            
            # Escape if levels meet or time exceeds 24h
            if head_diff <= 0 or minutes_elapsed > 1440: break

    hours_required = minutes_elapsed / 60
    avg_flow_rate = np.mean(rates_used) if rates_used else 0.0

    # 4. Final Calculation
    gen_for_transfer = total_mcm_moved / u_rate

    # --- 5. RESULTS ---
    st.divider()
    st.header(f"BTRP PH Dispatch Target for Transfer: {gen_for_transfer:.3f} MUS")
    
    res1, res2 = st.columns(2)
    with res1:
        st.subheader("🏁 Rewalje Status")
        st.write(f"Current Level: **{curr_l:.3f} m**")
        st.write(f"Available Buffer: **{available_buffer_l:.3f} MCM**")
        st.write(f"Total Demand (0.28mus): **{total_needed_l_mcm:.3f} MCM**")
        
    with res2:
        st.subheader("🏁 Transfer Operation")
        if transfer_needed_mcm <= 0:
            st.success("✅ NO TRANSFER REQUIRED (Buffer is sufficient)")
        else:
            st.warning("🕒 GATE OPERATION REQUIRED")
            st.markdown(f"### OPEN GATES for: :red[{hours_required:.2f} Hours]")
            st.write(f"Net Deficit to cover: **{transfer_needed_mcm:.3f} MCM**")
            st.metric("BTRP Gen Req", f"{gen_for_transfer:.3f} MUS")

    with st.expander("Technical Log"):
        st.write(f"Initial Head Difference: **{curr_u - curr_l:.2f} m**")
        if rates_used:
            st.write(f"Avg. Flow Rate during convergence: **{avg_flow_rate:.3f} MCM/hr**")
            
