# Highway RLStudio

This application is designed to streamline the process of training, testing, and visualizing reinforcement learning models in user-customized environments. Built using **Streamlit** and **sqlite3**, it provides a step-by-step interface for configuring environments, defining model hyperparameters, managing training runs, exploring TensorBoard logs and testing the pretrained model for performance on **Highway ENV** Reinforcement Learning.


## Installation
Make sure you have installed `Conda`. Our project is using conda to configure the envrionment. You can create a conda virtual env first:

`conda create -n highway_pjt python=3.9.20`

After that, please install all the necessary packages using the following command:

`conda activate highway_pjt`

`pip install -r requirements.txt`

`cd HighwayEnv`

`pip install -e .`




## Usage
To run the app, you con following the below steps:

`conda activate highway_pjt`

`streamlit run Webapp3/app3.py`

Then the app will be launched in your default browser.