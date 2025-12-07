# Experimental Derivation of a Stochastic Wi-Fi Network Model for ROS2 NCS

### Bachelor's Thesis Project
* **Title:** Impact of Wireless Networks on Robot Control
* **Author:** Nicolò Martini
* **Supervisor:** Prof. Pietro Falco
* **University:** Università degli Studi di Padova
* **Year:** 2025

---

## 📖 Overview

This repository contains the source code, experimental datasets, and simulation models developed to characterize the impact of Wi-Fi 6 (IEEE 802.11ax) latency on ROS2-based Networked Control Systems (NCS).

The project follows an empirical black-box approach to derive a stochastic model of the One-Way Delay (OWD) and evaluates its effects on the stability of an industrial robot manipulator (ABB IRB120) using MATLAB Simulink.

### Key Features
* **Real-world Testbed:** C++ ROS2 package (`delay_est`) for measuring OWD with NTP synchronization.
* **Statistical Analysis:** Python scripts (`delay_anl`) for data fitting and asymmetry analysis on measured datasets.
* **Control Simulation:** MATLAB Simulink environment (`delay_sim`) comparing nominal vs networked control performance.

---

## 📂 Repository Structure

```text
ros2-wifi-stochastic-delay/
├── ros2_ws/               # C++ ROS2 workspace
│   └── src/
│       └── delay_est/     # ROS2 package for OWD estimation
│
├── delay_anl/             # Python analysis tools
│   ├── data.zip           # Compressed Experimental Datasets (Unzip required!)
│   ├── data_analysis.py   # Analysis script
│   └── environment.yml    # Conda environment file for reproducibility
│    
└── delay_sim/             # MATLAB Simulink Application
    ├── load_parameters.m  # Parameter initialization script
    ├── model.slx          # Simulink model
    ├── plot_results.m     # Tracking error and 3D trajectory plotting script
    ├── animate_robot.m    # Animation generation script
    └── results.mat        # Pre-computed simulation results
```

---

## 🛠️ Hardware & Software Setup

The experimental data was collected using the following setup:

* **Nodes:** 2x Raspberry Pi 4 Model B (4GB RAM)
* **OS:** Ubuntu 22.04 LTS Server (64bit)
* **Middleware:** ROS2 Humble Hawksbill
* **Network:** TP-Link AX1500 (Wi-Fi 6 Access Point)
* **Synchronization:** Local NTP Server via Ethernet (Chronyd)

---

## 🚀 Usage Guide

### 1. Data Acquisition (ROS2)
Navigate to the workspace and build the package:
```bash
cd ros2_ws
colcon build --packages-select delay_est
source install/setup.bash

# Run the delay estimation nodes (example)
ros2 run delay_est sender
ros2 run delay_est receiver
```
*Note: Ensure NTP synchronization is active between nodes before running measurements.*

### 2. Statistical Analysis (Python)
The `delay_anl` folder contains the experimental datasets compressed in `data.zip` and the analysis scripts. The Python environment is managed via Anaconda.

To replicate the exact analysis environment, a frozen `environment.yml` file is provided.

```bash
cd delay_anl

# Unzip the datasets
unzip data.zip

# Create the environment from the file
conda env create -f environment.yml

# Activate the environment
conda activate delay-analysis

# Run the analysis
python3 data_analysis.py
```

### 3. Simulation (MATLAB)
**Requirements:** MATLAB R2025b with the following toolboxes installed:
* Robotics System Toolbox (Required for `RigidBodyTree` dynamics and kinematics)
* Control System Toolbox (Required for controller implementation and analysis)

**Steps:**
1.  Open MATLAB and navigate to the `delay_sim` folder.
2.  Run `load_parameters.m` to initialize all the model parameters.
3.  Open and run `model.slx` to perform the simulation.
4.  Visualization:
    * run `plot_results.m` to view tracking error divergence and trajectory comparison.
    * run `animate_robot.m` to generate the video/frames of the simulation.
    * *(Note: you can use `results.mat` to plot data without re-running the simulation).*

---

## 📊 Key Results

* **Distribution & Payload Dependency:** for typical control traffic (small payloads), the OWD follows a Lognormal distribution, characterized by heavy tails. As the payload size increases, the distribution shape evolves, transitioning towards a central distribution.
* **Asymmetry:** the channel is statistically asymmetric ($OWD_{AB} \neq OWD_{BA}$).
* **Impact:** introducing the stochastic delay model in the control loop causes a violation of the phase margin, leading to instability in the standard PD controller.

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
