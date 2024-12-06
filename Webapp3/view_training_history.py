import streamlit as st
import sqlite3
import json
import os
from subprocess import Popen
import time

def visualize_tensorboard(run_id):
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute('SELECT log_path FROM training_history WHERE id = ?', (run_id,))
    row = c.fetchone()
    conn.close()

    log_path = row[0]

    st.write(f"Launching TensorBoard for log path: {log_path}")
    tensorboard_process = Popen(["tensorboard", "--logdir", log_path, "--port", "6006"], stdout=None, stderr=None)

    time.sleep(3)
    st.components.v1.iframe(src="http://localhost:6006", height=800, scrolling=True)

    if st.button("Stop TensorBoard"):
        tensorboard_process.terminate()
        st.success("TensorBoard stopped.")


def delete_training_configuration(run_id):
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute('DELETE FROM training_history WHERE id = ?', (run_id,))
    conn.commit()
    conn.close()
    st.success(f"Deleted training configuration Run ID {run_id} successfully!")
    st.experimental_set_query_params(refresh="true") 
    st.stop()

def load_training_configuration(run_id):
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()

    c.execute('SELECT env_name, env_params, model_name, model_params FROM training_history WHERE id = ?', (run_id,))
    row = c.fetchone()
    conn.close()

    st.session_state["selected_env"] = row[0]
    st.session_state["env_params"] = json.loads(row[1])
    st.session_state["model"] = row[2]
    st.session_state["model_params"] = json.loads(row[3])

    st.success(f"Configuration for Run ID {run_id} loaded successfully!")

def view_training_history():
    st.header("Training History")
    
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute('SELECT id, model_path, env_name, training_steps, timestamp, log_path FROM training_history')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        st.write(f"ID: {row[0]}")
        st.write(f"Model Path: {row[1]}")
        st.write(f"Environment: {row[2]}")
        st.write(f"Training Steps: {row[3]}")
        st.write(f"Timestamp: {row[4]}")
        st.write(f"Log Path: {row[5]}")
        # if st.button(f"Load Configuration for ID {row[0]}"):
        #     load_training_configuration(row[0])
        if st.button(f"View Logs for ID {row[0]}", key=f"view_logs_{row[0]}"):
            visualize_tensorboard(row[0])
        if st.button(f"Delete Entry ID {row[0]}", key=f"delete_entry_{row[0]}"):
            delete_training_configuration(row[0])
            st.experimental_rerun() 
