
#  Differential Privacy Demo – Walkthrough

This walkthrough explains how the DP demo is structured and what each component does.

---

##  Files Overview

You have two main model training scripts:

1. **`baseline_model.py`** — Regular model with no privacy
2. **`dp_model.py`** — Differentially private model using TensorFlow Privacy

And a visual React demo file:

- **`dp_demo.jsx`** — Interactive privacy vs accuracy visualizer

---

##  Baseline Model (`baseline_model.py`)

This is a standard training script for the MNIST dataset.

### 🔍 What It Does:
- Loads and normalizes the MNIST dataset
- Flattens the 28x28 images into 784-pixel vectors
- Defines a basic neural network:
  ```python
  tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(784,)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10)
  ])
  ```
- Compiles the model with:
  - `SparseCategoricalCrossentropy` loss
  - `Adam` optimizer
- Trains using `.fit()` and evaluates accuracy on the test set

###  Result:
- **High accuracy (~97.86%)**
- **No privacy protection**
- Represents a best-case performance baseline

---

##  DP Model (`dp_model.py`)

This version uses Differential Privacy to protect individual training examples.

###  What It Changes:
- Uses `DPKerasSGDOptimizer`:
  ```python
  DPKerasSGDOptimizer(
      l2_norm_clip=1.0,
      noise_multiplier=1.1,
      num_microbatches=256,
      learning_rate=0.25
  )
  ```
- Adds noise to gradients and clips them to limit individual impact
- Requires loss reduction set to `NONE` to compute per-example gradients:
  ```python
  loss = tf.keras.losses.SparseCategoricalCrossentropy(
      from_logits=True,
      reduction=tf.keras.losses.Reduction.NONE
  )
  ```
- Trains as usual with `.fit()`
- Uses `compute_dp_sgd_privacy()` to compute **ε (epsilon)**

### 📉 Result:
- **Accuracy ~91.91%**
- **Privacy Guarantee: ε = 1.28**
- Shows privacy-accuracy tradeoff

---

## What the Demo Shows

- **Privacy–Accuracy Tradeoff** is real and tunable
- **ε (Epsilon)** is a measurable privacy budget
- **Differential Privacy is practical** — not just theory
- **Baseline vs DP** comparison is key for understanding model hardening

