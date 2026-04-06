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
st.set_page_config(page_title="Gate Operation Control", layout="wide")
st.title("🚧 Gate Operation & Closure Advisor")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Upper Reservoir (Source)")
    curr_u = st.number_input("Current Upper RL (m)", value=93.400, format="%.3f")
    lake_ph_rate = 0.820 

with col2:
    st.subheader("📍 Lower Reservoir (Target)")
    curr_l = st.number_input("Current Lower RL (m)", value=92.000, format="%.3f")
    l_gen_target = st.number_input("Lower PH Planned Gen (MUS)", value=0.120, format="%.3f")
    l_ph_rate = 9.360 

# --- 4. CALCULATION ---
if st.button("Analyze Gate Status", type="primary"):
    
    # Safety Check
    if curr_l < 90.000:
        st.error("🚨 ALERT: Lower Res below 90m limit. Keep gates open to recover level!")
    else:
        # A. Calculate total water needed in Lower Res
        lower_ph_demand = l_gen_target * l_ph_rate
        
        # B. Gate Calculation (Based on 3-tier head-dependent rules)
    gate_vol = 0.0
    if gate_is_open:
        head_diff = u_level_in - l_level_in
        
        # Define flow rate based on head tiers
        if head_diff > 3.0:
            rate = 0.17  # MCM/hr for head > 3m
        elif 2.0 <= head_diff <= 3.0:
            rate = 0.15  # MCM/hr for head between 2m and 3m
        elif 1.5 <= head_diff < 2.0:
            rate = 0.12  # MCM/hr for head between 1.5m and 2m
        else:
            rate = 0.08  # Fallback for head < 1.5m
            
        gate_vol = rate * hours_open

        
        # C. Estimate time to close
        # Time (hrs) = Water Needed (MCM) / Flow Rate (MCM/hr)
        time_to_close = lower_ph_demand / current_flow_rate
        
        # D. Upper Res Impact
        target_u_mcm = 8.067 # for 94.50m
        idx_u = (np.abs(u_rl_table - curr_u)).argmin()
        start_u_mcm = u_mcm_table[idx_u]
        u_gap = target_u_mcm - start_u_mcm
        
        # Total Gen required at Lake PH
        total_release_mcm = u_gap + lower_ph_demand
        lake_gen_required = total_release_mcm / lake_ph_rate

        # --- 5. ADVISORY OUTPUTS ---
        st.divider()
        
        c_advise, c_gen = st.columns(2)
        
        with c_advise:
            st.header("🏁 Gate Recommendation")
            if time_to_close <= 0:
                st.success("✅ CLOSE GATES NOW: Lower Reservoir has sufficient water.")
            else:
                st.warning(f"🕒 KEEP GATES OPEN: Close in {time_to_close:.2f} Hours.")
                st.info(f"Targeting {lower_ph_demand:.3f} MCM transfer at {current_flow_rate} MCM/hr.")

        with c_gen:
            st.header("⚡ Generation Target")
            st.metric("Lake PH Total Gen", f"{lake_gen_required:.3f} MUS")
            st.caption(f"This gen includes {u_gap:.3f} MCM for your 94.50m level goal.")

        with st.expander("View Logic Details"):
            st.write(f"Lower PH Target: {l_gen_target} MUS requires **{lower_ph_demand:.3f} MCM**.")
            st.write(f"With a {head_diff:.2f}m head, flow is **{current_flow_rate} MCM/hr**.")
            st.write(f"Upper Res filling needs **{u_gap:.3f} MCM**.")
