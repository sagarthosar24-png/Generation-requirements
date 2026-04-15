import streamlit as st
import numpy as np

# --- 1. RESERVOIR STORAGE DATA (MCM) ---
# Ensure these dictionaries contain your full datasets
u_data = {
    90.000: 4.336, 90.025: 4.354, 90.050: 4.371, 90.075: 4.389, 90.100: 4.406,
    90.125: 4.424, 90.150: 4.441, 90.175: 4.459, 90.200: 4.476, 90.225: 4.494,
    90.250: 4.511, 90.275: 4.529, 90.300: 4.546, 90.325: 4.564, 90.350: 4.581,
    90.375: 4.599, 90.400: 4.616, 90.425: 4.634, 90.450: 4.651, 90.475: 4.669,
    90.500: 4.686, 90.525: 4.704, 90.550: 4.721, 90.575: 4.739, 90.600: 4.756,
    90.625: 4.774, 90.650: 4.791, 90.675: 4.809, 90.700: 4.826, 90.725: 4.844,
    90.750: 4.861, 90.775: 4.879, 90.800: 4.896, 90.825: 4.914, 90.850: 4.931,
    90.875: 4.949, 90.900: 4.966, 90.925: 4.984, 90.950: 5.001, 90.975: 5.019,
    91.000: 5.036, 91.025: 5.054, 91.125: 5.124, 91.250: 5.211, 91.375: 5.299,
    91.500: 5.386, 91.625: 5.474, 91.750: 5.561, 91.875: 5.649, 92.000: 5.736,
    92.250: 5.936, 92.500: 6.137, 92.750: 6.338, 93.000: 6.539, 93.250: 6.739,
    93.500: 6.940, 93.750: 7.141, 94.000: 7.342, 94.250: 7.535, 94.400: 7.862,
    94.500: 8.067, 94.750: 8.579, 95.000: 9.081
}

l_data = {
    89.000: 2.870, 89.250: 2.975, 89.500: 3.080, 89.750: 3.185, 90.000: 3.290,
    90.250: 3.345, 90.500: 3.400, 90.750: 3.520, 91.000: 3.640, 91.250: 3.765,
    91.500: 3.890, 91.750: 3.955, 92.000: 4.020, 92.250: 4.135, 92.500: 4.250,
    92.750: 4.365, 93.000: 4.480, 93.250: 4.570, 93.500: 4.660, 93.750: 4.750,
    94.000: 4.840, 94.250: 4.945, 94.500: 5.050, 94.750: 5.495, 95.000: 5.940
}

# --- 2. GATE DISCHARGE DATA (Head Diff vs Flow) ---
# Key: Head Diff (m), Value: Flow (m3/sec)
head_flow_lookup = {
    0.000: 0.00, 0.063: 2.50, 0.125: 5.00, 0.188: 7.50, 0.250: 10.00,
    0.313: 12.50, 0.375: 15.00, 0.438: 17.50, 0.500: 20.00, 0.563: 20.75,
    0.625: 21.50, 0.688: 22.25, 0.750: 23.00, 0.813: 23.75, 0.875: 24.50,
    0.938: 25.25, 1.000: 26.00, 1.125: 27.50, 1.250: 29.00, 1.375: 30.50,
    1.500: 32.00, 1.625: 33.50, 1.750: 35.00, 1.875: 36.50, 2.000: 38.00,
    2.125: 39.13, 2.250: 40.25, 2.375: 41.38, 2.500: 42.50, 2.625: 43.63,
    2.750: 44.75, 2.875: 45.88, 3.000: 47.00, 3.125: 48.00, 3.250: 49.00,
    3.375: 50.00, 3.500: 51.00, 3.625: 52.00, 3.750: 53.00, 3.875: 54.00,
    4.000: 55.00, 4.125: 56.00, 4.250: 57.00, 4.375: 58.00, 4.500: 59.00,
    4.625: 60.00, 4.750: 61.00, 4.875: 62.00, 5.000: 63.00
}

def get_flow_mcm_hr(head_diff):
    """Interpolates flow in m3/s and converts to MCM/hr."""
    heads = sorted(head_flow_lookup.keys())
    flows = [head_flow_lookup[h] for h in heads]
    flow_m3s = np.interp(head_diff, heads, flows)
    return flow_m3s * (3600 / 1000000)

# --- 3. STREAMLIT APP ---
st.set_page_config(page_title="BTRP-Rewalje Dispatch", layout="wide")
st.title("⚡ Dynamic Operational Shift Planner")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 BTRP DAM (Upper)")
    curr_u = st.number_input("Current Level (m)", value=94.400, format="%.3f")
    u_rate = 0.820  # MCM/MUS

with col2:
    st.subheader("📍 Rewalje Forebay (Lower)")
    curr_l = st.number_input("Current Level (m) ", value=92.500, format="%.3f")
    l_gen_req = st.number_input("Planned Rewalje Gen (MUS)", value=0.080, format="%.3f")
    l_conversion = 9.360 # MCM/MUS

# --- 4. CORE CALCULATIONS ---
if st.button("Generate Dispatch Report", type="primary"):
    
    # Target Constants
    U_TARGET_MCM = 8.067 # Target for RL 94.500
    L_FLOOR_MCM = 3.290  # Floor for RL 90.000
    L_FSL_RL = 94.500    # Full Supply Level
    
    # Initial State
    u_keys = np.array(list(u_data.keys()))
    l_keys = np.array(list(l_data.keys()))
    l_mcm_vals = np.array(list(l_data.values()))
    
    start_u_mcm = u_data[u_keys[(np.abs(u_keys - curr_u)).argmin()]]
    start_l_mcm = l_data[l_keys[(np.abs(l_keys - curr_l)).argmin()]]

    # Deficit Logic
    demand_l = l_gen_req * l_conversion
    available_l = start_l_mcm - L_FLOOR_MCM
    transfer_needed = max(0.0, demand_l - available_l)
    
    # DYNAMIC SIMULATION (1-minute steps for precision)
    sim_u_mcm = start_u_mcm
    sim_l_mcm = start_l_mcm
    total_moved = 0.0
    minutes = 0
    flow_history = []
    
    if transfer_needed > 0:
        while total_moved < transfer_needed:
            # Map current storage back to levels to find Head
            u_rl_now = u_keys[(np.abs(np.array(list(u_data.values())) - sim_u_mcm)).argmin()]
            l_rl_now = l_keys[(np.abs(l_mcm_vals - sim_l_mcm)).argmin()]
            head_diff = u_rl_now - l_rl_now
            
            # Look up flow rate based on table
            flow_hr = get_flow_mcm_hr(head_diff)
            flow_history.append(flow_hr)
            
            # Advance simulation by 1 minute
            step_mcm = flow_hr / 60
            remaining = transfer_needed - total_moved
            
            if step_mcm >= remaining:
                # Calculate precise fraction of the last minute
                fraction = remaining / step_mcm if step_mcm > 0 else 1
                minutes += fraction
                sim_l_mcm += remaining
                total_moved = transfer_needed
            else:
                minutes += 1
                total_moved += step_mcm
                sim_u_mcm -= step_mcm
                sim_l_mcm += step_mcm
            
            if head_diff <= 0 or minutes > 2880: break # Safety exit

    # Predicted Final States
    final_l_rl = l_keys[(np.abs(l_mcm_vals - sim_l_mcm)).argmin()]
    gen_for_transfer = transfer_needed / u_rate
    gen_for_level = (U_TARGET_MCM - start_u_mcm) / u_rate
    total_btrp_gen = gen_for_level + gen_for_transfer

    # --- 5. REPORTING ---
    st.divider()
    
    # SAFETY ALERTS
    if final_l_rl >= L_FSL_RL:
        st.error(f"🚨 OVERFLOW RISK: Rewalje will reach {final_l_rl:.3f}m. Max is {L_FSL_RL}m.")
    elif final_l_rl >= 94.200:
        st.warning(f"⚠️ HIGH LEVEL: Predicted Rewalje Level {final_l_rl:.3f}m.")
    else:
        st.success(f"✅ Predicted Rewalje level is safe ({final_l_rl:.3f}m).")

    # PRIMARY RESULTS
    res_btrp, res_gate = st.columns(2)
    
    with res_btrp:
        st.header(f"BTRP Dispatch: {max(0, total_btrp_gen):.3f} MUS")
        st.write(f"Leveling Component: {gen_for_level:.3f} MUS")
        st.write(f"Transfer Component: {gen_for_transfer:.3f} MUS")
        
    with res_gate:
        if transfer_needed > 0:
            st.header(f"Gate Time: :red[{minutes/60:.2f} Hours]")
            st.write(f"Volume to Transfer: **{transfer_needed:.3f} MCM**")
            st.write(f"Avg. Flow Rate: **{np.mean(flow_history) if flow_history else 0:.4f} MCM/hr**")
        else:
            st.header("Gate Time: :green[CLOSED]")
            st.write("No transfer required to meet demand.")

    with st.expander("Show Simulation Log"):
        st.write(f"Initial Head: {curr_u - curr_l:.2f} m")
        st.write(f"Starting MCM (U/L): {start_u_mcm:.3f} / {start_l_mcm:.3f}")
        st.write(f"Final Predicted MCM (L): {sim_l_mcm:.3f}")
