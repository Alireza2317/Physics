# Physics Simulations with Python

![Python](https://img.shields.io/badge/python-gray?logo=python)
![Pymunk](https://img.shields.io/badge/Physics-Pymunk-green)
![Pygame](https://img.shields.io/badge/Render-Pygame-yellow)
![License](https://img.shields.io/badge/license-MIT-grey)

A collection of interactive 2D physics simulations built using **Pymunk** (physics engine) and **Pygame** (rendering). These scripts visualize fundamental concepts in mechanics, chaos theory, and statistics.

## 🧪 Simulations & Demos

### 1. Double Pendulum (Chaos Theory)
A simulation of a pendulum with another pendulum attached to its end. It demonstrates **chaotic motion**, where the system is highly sensitive to initial conditions.
<p align="center">
  <img src="https://github.com/user-attachments/assets/c30f1915-650a-4be5-8f5a-7f339e3f2bee" alt="Double Pendulum Demo" width="600">
</p>

### 2. Galton Board (Probability)
A vertical board with interleaved rows of pegs. Balls drop from the top, bouncing randomly left or right. It demonstrates how the **Binomial Distribution** approximates the **Normal Distribution** (Bell Curve) as the number of balls increases.
<p align="center">
  <img src="https://github.com/user-attachments/assets/ba3bd69b-ce95-4c9c-9a17-b47ec66db8d5" alt="Double Pendulum Demo" width="600">
</p>

### 3. Simple Pendulum (Harmonic Motion)
A classic simulation of a simple pendulum subject to gravity and damping, visualizing the conversion between potential and kinetic energy.
<p align="center">
  <img src="https://github.com/user-attachments/assets/42ae076b-fcc8-4281-8275-1d35860176ba" alt="Simple Pendulum Demo" width="600">
</p>

## 🛠️ Requirements

* **Python 3**
* **Pymunk:** 2D rigid body physics library.
* **Pygame:** Library for making visuals.

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/Alireza2317/Physics](https://github.com/Alireza2317/Physics)
cd Physics

# Install required libraries
pip install -r requirements.txt
```

### 2. Usage
Navigate to the specific folder and run the script:

```Bash
# Example: Running the Double Pendulum
cd double_pendulum
python app.py
```

## 📂 Project Structure
```text
.
├── double_pendulum/     # Chaos theory simulation
├── galton_board/        # Statistical distribution simulation
├── pendulum/            # Simple harmonic motion
└── requirements.txt
```




