# 🌡️ Python Black Body Radiation Simulator

An interactive GUI simulation of **black body radiation** built with Python, Tkinter, and Matplotlib. Visualize Planck's Law in real time — adjust temperature from 1,000 K to 30,000 K and watch the spectral curve, peak wavelength, and apparent color update live with a pulsing animated glow effect.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Physics](https://img.shields.io/badge/Physics-Quantum%20Thermodynamics-purple?style=flat-square)

---

## 📌 Table of Contents

- [About](#about)
- [Physics Background](#physics-background)
- [Key Formulas Used](#key-formulas-used)
- [Modules Used](#modules-used)
- [Getting Started](#getting-started)
- [Features](#features)
- [Project Structure](#project-structure)
- [References](#references)

---

## About

This simulator models the electromagnetic radiation emitted by a **perfect black body** — an idealized object that absorbs all incoming radiation and re-emits energy purely as a function of temperature. The simulation is built around three foundational laws of physics and renders results in real time through an interactive GUI.

---

## Physics Background

### What is a Black Body?

A **black body** is an idealized object that:
- Absorbs **100%** of all incident electromagnetic radiation
- Emits radiation **only** based on its temperature — not its material, shape, or surface color

Real-world approximations: the Sun, stars, glowing coals, and heated metal. The spectrum they produce is called **black body radiation** or **thermal radiation**.

---

### The Ultraviolet Catastrophe

Before 1900, classical physics (the Rayleigh–Jeans Law) predicted that a black body should emit **infinite energy** at short (ultraviolet) wavelengths — an obviously absurd result known as the **Ultraviolet Catastrophe**.

In 1900, **Max Planck** solved this by proposing that energy is not emitted continuously but in discrete packets called **quanta**. This was the birth of **quantum mechanics**.

---

### Planck's Law

Planck's Law gives the **spectral radiance** — power emitted per unit area, per unit wavelength, per steradian — of a black body at temperature *T*:

```
B(λ, T) = (2hc² / λ⁵) × 1 / (exp(hc / λk_B T) − 1)
```

| Symbol | Meaning | Value |
|--------|---------|-------|
| `λ` | Wavelength (m) | variable |
| `T` | Temperature (K) | variable |
| `h` | Planck's constant | 6.626 × 10⁻³⁴ J·s |
| `c` | Speed of light | 3.0 × 10⁸ m/s |
| `k_B` | Boltzmann constant | 1.381 × 10⁻²³ J/K |

The **exponential term** in the denominator is what prevents the ultraviolet catastrophe — as λ → 0, the exponential grows far faster than the λ⁵ term, driving radiance back to zero at short wavelengths.

---

### Wien's Displacement Law

The wavelength at which a black body emits **maximum energy** shifts inversely with temperature:

```
λ_max = b / T
```

Where `b = 2.898 × 10⁻³ m·K` is Wien's displacement constant.

| Object | Temperature | Peak λ |
|--------|-------------|--------|
| Human body | ~310 K | ~9,350 nm (far infrared) |
| Incandescent bulb | ~3,000 K | ~966 nm (near infrared) |
| The Sun | ~5,778 K | ~502 nm (visible green) |
| Blue-white star | ~20,000 K | ~145 nm (ultraviolet) |

This is why heated metal glows red → orange → white → blue-white as it gets hotter, and why stars appear in different colors across the night sky.

---

### Stefan–Boltzmann Law

The **total power** radiated per unit surface area across all wavelengths is:

```
P = σ T⁴
```

Where `σ = 5.67 × 10⁻⁸ W·m⁻²·K⁻⁴` is the Stefan–Boltzmann constant.

The T⁴ dependence is dramatic — doubling the temperature increases total emitted power by **16×**. The simulator displays this relative to the Sun (5000 K reference) in real time.

---

### Why Does Color Change With Temperature?

As temperature rises:
1. Peak wavelength shifts from infrared → red → orange → yellow → white → blue-white
2. Total power scales as T⁴
3. The visible fraction of the emitted spectrum grows

This is physically modeled in `get_blackbody_color()`, which maps temperature to approximate RGB through piecewise linear interpolation across the 1,000 K–30,000 K range. The `wavelength_to_rgb()` function converts individual visible-light wavelengths (380–780 nm) to RGB using CIE color matching approximations, producing the rainbow gradient overlay on the plot.

---

## Key Formulas Used

### 1. Planck's Law — core simulation engine
```python
def planck_law(lam, T):
    lam_m = lam * 1e-9          # convert nm → meters
    return (2 * h * c**2 / lam_m**5) * (1 / (np.exp(h * c / (lam_m * k * T)) - 1))
```
Computes spectral radiance at every wavelength point for a given temperature. Called on 800-point arrays via NumPy vectorization.

### 2. Wien's Displacement Law — peak wavelength label
```python
lambda_max = b_wien / self.temperature * 1e9  # result in nm
```
Displayed live in the stats bar as `λ_max: XXX nm`.

### 3. Stefan–Boltzmann — relative radiated power
```python
relative_power = (self.temperature / 5000) ** 4
```
Normalized to 5000 K as a solar reference, displayed as `Power: X.XXσT⁴`.

---

## Modules Used

| Module | Purpose |
|--------|---------|
| `tkinter` | Core GUI framework — window, slider, buttons, labels, canvas |
| `tkinter.ttk` | Themed widget styles for the temperature slider |
| `matplotlib` | Spectrum plot rendering (Planck curve + gradient band) |
| `matplotlib.backends.backend_tkagg` | Embeds the Matplotlib `Figure` inside the Tkinter window |
| `matplotlib.figure.Figure` | Creates the dark-themed spectral radiance figure |
| `numpy` | Vectorized Planck computation, `linspace` for wavelength arrays, `sin` for glow animation |

All dependencies are part of the standard scientific Python stack — no third-party installs beyond `matplotlib` and `numpy`.

---

## Getting Started

### Prerequisites

```bash
pip install matplotlib numpy
```

> `tkinter` ships with standard Python on Windows and macOS. On Linux:
> ```bash
> sudo apt-get install python3-tk
> ```

### Run

```bash
git clone https://github.com/parthakk07/python-blackbody-simulation.git
cd python-blackbody-simulation
python blackbody_sim.py
```

The GUI window (1100 × 680 px) will launch immediately.

---

## Features

- **Live Planck curve** — spectral radiance plotted from 100 nm to 1600 nm, normalized and redrawn on every slider change
- **Animated pulsing glow** — a secondary glow line pulses sinusoidally at ~60 fps to visualize radiated energy
- **Apparent color indicator** — a colored circle showing the perceived color of the black body at the current temperature, computed via `get_blackbody_color()`
- **Rainbow visible spectrum band** — the 380–780 nm region is overlaid with a CIE-approximated color gradient
- **IR / Visible / UV region labels** — physical context annotations directly on the plot
- **Wien's λ_max display** — peak wavelength updated live in the stats bar
- **Stefan–Boltzmann power display** — relative power normalized to 5000 K reference
- **Temperature presets** — one-click buttons for five iconic objects:

  | Preset | Temperature | Color |
  |--------|-------------|-------|
  | Iron | 1,000 K | Deep red |
  | Candle | 3,000 K | Warm orange |
  | Sun | 5,000 K | Yellow |
  | Daylight | 6,500 K | Near-white |
  | Blue Star | 10,000 K | Light blue |

- **Dark GitHub-style theme** — `#0d1117` background optimized for accurate color representation

---

## Project Structure

```
python-blackbody-simulation/
│
├── blackbody_sim.py       # All physics, GUI, and animation in one file
└── README.md
```

### Key Components

| Name | Type | Role |
|------|------|------|
| `BlackBodySimulator` | Class | Main app — builds GUI, handles events, runs animation loop |
| `planck_law(lam, T)` | Function | Computes spectral radiance via Planck's equation |
| `wavelength_to_rgb(wavelength)` | Function | Converts nm → RGB for the visible spectrum gradient overlay |
| `get_blackbody_color(T)` | Function | Maps temperature → approximate perceived RGB color |
| `update_simulation()` | Method | Redraws the Planck curve, color circle, and all stat labels |
| `run_animation()` | Method | Recursive `root.after(16, ...)` loop driving the glow pulse at ~60 fps |

---

## Physical Constants

```python
h      = 6.626e-34   # Planck's constant      (J·s)
c      = 3.0e8       # Speed of light          (m/s)
k      = 1.381e-23   # Boltzmann constant      (J/K)
b_wien = 2.898e-3    # Wien's displacement     (m·K)
```

---

## References

- Planck, M. (1901). *On the Law of Distribution of Energy in the Normal Spectrum*. Annalen der Physik.
- Wien, W. (1893). *A New Relationship Between the Radiation from a Black Body and the Second Law of Thermodynamics*.
- [NIST Physical Constants](https://physics.nist.gov/cuu/Constants/)
- [HyperPhysics — Black Body Radiation](http://hyperphysics.phy-astr.gsu.edu/hbase/mod6.html)

---

*Built with Python · Physics by Planck, Wien & Stefan–Boltzmann*
