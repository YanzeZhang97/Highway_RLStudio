import streamlit as st
from step1_config_env import run as step1
from step2_modelparameters import run as step2
from step3_model_path import run as step3
from step4_log_path import run as step4
from step5_training import run as step5
from step6_testing import run as step6

# Sidebar navigation
st.sidebar.title("Navigation Bar")
options = ["Step 1: Config Env", "Step 2: Modelparameters", 
           "Step 3: Model Path", "Step 4: Log Path", 
           "Step 5: Start Training",
           "Step 6: Testing"]
selection = st.sidebar.radio("Go to", options)

# Display the selected page
if selection == "Step 1: Config Env":
    step1()
elif selection == "Step 2: Modelparameters":
    step2()
elif selection == "Step 3: Model Path":
    step3()
elif selection == "Step 4: Log Path":
    step4()
elif selection == "Step 5: Start Training":
    step5()
elif selection == "Step 6: Testing":
    step6()




