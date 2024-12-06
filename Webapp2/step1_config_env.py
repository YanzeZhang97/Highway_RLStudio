import streamlit as st



def run():
    st.header("Step 1: Configure Environment")
    
    # Environment selection
    ENVIRONMENTS = ["highway-v0", "merge-v0", "roundabout-v0", "intersection-v0"]
    selected_env = st.selectbox("Choose an environment:", ENVIRONMENTS)
    st.session_state["selected_env"] = selected_env
    
    # Advanced configuration for "highway-v0"
    if selected_env == "highway-v0":
        st.subheader("Highway-v0 Configuration")
        spacing = st.number_input(
            "Vehicle Spacing:", 
            min_value=0, max_value=10, value=2, step=1
        )
        st.session_state["spacing"] = spacing
        num_vehicles = st.number_input(
            "Number of Vehicles:", 
            min_value=1, max_value=100, value=50, step=1
        )
        st.session_state["num_vehicles"] = num_vehicles
        num_lanes = st.number_input(
            "Number of Lanes:", 
            min_value=1, max_value=10, value=4, step=1
        )
        st.session_state["num_lanes"] = num_lanes
        render = st.selectbox("off-screen render or not:", options=[True, False])
        # render = st.selectbox('off-screen render or not', trueorfalse)
        st.session_state["rendering"] = render

        st.write("### Selected Configuration")
        st.write(f"Environment: {selected_env}")
        st.write(f"Vehicle Spacing: {spacing}")
        st.write(f"Number of Vehicles: {num_vehicles}")
        st.write(f"Number of Lanes: {num_lanes}")
        st.write(f"Off-screen rendering: {render}")
    if selected_env == "merge-v0":
        st.subheader("Merge-v0 Configuration")
        render = st.selectbox("off-screen render or not:", options=[True, False])
        # render = st.selectbox('off-screen render or not', trueorfalse)
        st.session_state["rendering"] = render

        st.write("### Selected Configuration")
        st.write(f"Off-screen rendering: {render}")

    if selected_env == "roundabout-v0":
        st.subheader("Roundabout-v0 Configuration")
        render = st.selectbox("off-screen render or not:", options=[True, False])
        # render = st.selectbox('off-screen render or not', trueorfalse)
        st.session_state["rendering"] = render

        st.write("### Selected Configuration")
        st.write(f"Off-screen rendering: {render}")
    
    if selected_env == "intersection-v0":
        st.subheader("Intersection-v0 Configuration")
        render = st.selectbox("off-screen render or not:", options=[True, False])
        # render = st.selectbox('off-screen render or not', trueorfalse)
        st.session_state["rendering"] = render

        st.write("### Selected Configuration")
        st.write(f"Off-screen rendering: {render}")

