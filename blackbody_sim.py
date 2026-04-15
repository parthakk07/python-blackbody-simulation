import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Physical constants
h = 6.626e-34
c = 3.0e8
k = 1.381e-23
b_wien = 2.898e-3

VISIBLE_MIN, VISIBLE_MAX = 380, 780


def planck_law(lam, T):
    lam_m = lam * 1e-9
    return (2 * h * c**2 / lam_m**5) * (1 / (np.exp(h * c / (lam_m * k * T)) - 1))


def wavelength_to_rgb(wavelength):
    if wavelength < 380 or wavelength > 780:
        return (0.05, 0.05, 0.05)
    if wavelength < 440:
        ratio = (440 - wavelength) / 60
    elif wavelength < 490:
        ratio = (wavelength - 440) / 50
    elif wavelength < 510:
        ratio = 1.0
    elif wavelength < 580:
        ratio = (580 - wavelength) / 70
    elif wavelength < 645:
        ratio = (wavelength - 580) / 65
    else:
        ratio = 0.0

    if wavelength < 420:
        intensity = 0.3 + 0.7 * (wavelength - 380) / 40
    elif wavelength > 700:
        intensity = 0.3 + 0.7 * (780 - wavelength) / 80
    else:
        intensity = 1.0

    if wavelength < 490:
        r, g, b = ratio * intensity, intensity, 1.0 * intensity
    elif wavelength < 510:
        r, g, b = 0.0, intensity, (1.0 - ratio) * intensity
    elif wavelength < 580:
        r, g, b = ratio * intensity, intensity, 0.0
    elif wavelength < 645:
        r, g, b = intensity, (1.0 - ratio) * intensity, 0.0
    else:
        r, g, b = intensity, 0.0, 0.0

    return (r, g, b)


def get_blackbody_color(T):
    if T < 1000:
        return (0.12, 0.02, 0.02)
    elif T < 2000:
        return ((T - 1000) / 1000 * 0.9, 0.02, 0.02)
    elif T < 3500:
        t = (T - 2000) / 1500
        return (0.9 + t * 0.1, t * 0.25, 0.0)
    elif T < 5000:
        t = (T - 3500) / 1500
        return (1.0, 0.25 + t * 0.35, t * 0.08)
    elif T < 6500:
        t = (T - 5000) / 1500
        return (1.0, 0.6 + t * 0.25, 0.08 + t * 0.15)
    elif T < 10000:
        t = (T - 6500) / 3500
        return (1.0 - t * 0.15, 0.85 + t * 0.1, 0.23 + t * 0.55)
    else:
        t = min((T - 10000) / 10000, 1.0)
        return (1.0 - t * 0.25, 0.95 - t * 0.1, 0.78 + t * 0.22)


class BlackBodySimulator:
    def __init__(self, root):
        self.root = root
        root.title("Black Body Radiation Simulator")
        root.geometry("1100x680")
        root.configure(bg="#0d1117")
        root.resizable(False, False)

        self.temperature = 5000
        self.animation_phase = 0

        self.setup_styles()
        self.setup_gui()
        self.update_simulation()
        self.run_animation()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScale", background="#161b22", troughcolor="#21262d")
        style.configure(
            "Horizontal.TScale", background="#161b22", troughcolor="#21262d"
        )

    def setup_gui(self):
        # Left panel - Controls
        left_panel = tk.Frame(self.root, bg="#161b22", width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        left_panel.pack_propagate(False)

        # Header
        header = tk.Frame(left_panel, bg="#161b22")
        header.pack(fill=tk.X, pady=(24, 8))

        tk.Label(
            header,
            text="Black Body",
            font=("SF Pro Display", 22, "bold"),
            bg="#161b22",
            fg="#f0f6fc",
        ).pack()

        tk.Label(
            header,
            text="Radiation Simulator",
            font=("SF Pro Display", 14),
            bg="#161b22",
            fg="#8b949e",
        ).pack()

        # Temperature section
        temp_section = tk.Frame(left_panel, bg="#161b22")
        temp_section.pack(fill=tk.X, pady=(24, 0))

        tk.Label(
            temp_section,
            text="TEMPERATURE",
            font=("SF Pro Text", 10, "bold"),
            bg="#161b22",
            fg="#8b949e",
        ).pack(anchor="w", padx=24)

        self.temp_value_label = tk.Label(
            temp_section,
            text="5,000 K",
            font=("SF Pro Display", 36, "bold"),
            bg="#161b22",
            fg="#f0f6fc",
        )
        self.temp_value_label.pack(anchor="w", padx=24, pady=(4, 12))

        # Custom slider
        slider_frame = tk.Frame(temp_section, bg="#161b22")
        slider_frame.pack(fill=tk.X, padx=24, pady=(0, 8))

        self.temp_var = tk.IntVar(value=5000)
        self.temp_slider = tk.Scale(
            slider_frame,
            from_=1000,
            to=30000,
            variable=self.temp_var,
            orient=tk.HORIZONTAL,
            length=232,
            command=self.on_temp_change,
            bg="#161b22",
            fg="#f0f6fc",
            highlightbackground="#161b22",
            troughcolor="#30363d",
            activebackground="#e94560",
            sliderrelief=tk.FLAT,
            borderwidth=0,
        )
        self.temp_slider.pack()

        tk.Label(
            slider_frame,
            text="1,000 K                              30,000 K",
            font=("SF Pro Text", 9),
            bg="#161b22",
            fg="#484f58",
        ).pack()

        # Preset buttons
        presets_section = tk.Frame(left_panel, bg="#161b22")
        presets_section.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        tk.Label(
            presets_section,
            text="PRESETS",
            font=("SF Pro Text", 10, "bold"),
            bg="#161b22",
            fg="#8b949e",
        ).pack(anchor="w", padx=24, pady=(0, 10))

        presets_grid = tk.Frame(presets_section, bg="#161b22")
        presets_grid.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))

        for i in range(3):
            presets_grid.grid_rowconfigure(i, weight=1)
        for i in range(2):
            presets_grid.grid_columnconfigure(i, weight=1)

        presets = [
            ("Iron", 1000, "#792323"),
            ("Candle", 3000, "#9c4a1a"),
            ("Sun", 5000, "#c9a227"),
            ("Daylight", 6500, "#f5f5dc"),
            ("Blue Star", 10000, "#87ceeb"),
        ]

        for i, (name, temp, color) in enumerate(presets):
            row, col = i // 2, i % 2
            btn = tk.Button(
                presets_grid,
                text=f"{name}\n{temp:,}K",
                font=("SF Pro Text", 10),
                bg="#21262d",
                fg="#c9d1d9",
                activebackground=color,
                activeforeground="#0d1117",
                relief=tk.FLAT,
                bd=0,
                highlightbackground="#21262d",
                highlightcolor="#21262d",
                command=lambda t=temp: self.set_temperature(t),
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        # Right panel - Display
        right_panel = tk.Frame(self.root, bg="#0d1117")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Stats bar
        stats_bar = tk.Frame(right_panel, bg="#161b22", height=60)
        stats_bar.pack(fill=tk.X, padx=20, pady=(20, 0))
        stats_bar.pack_propagate(False)

        self.peak_label = tk.Label(
            stats_bar,
            text="λ_max: 580 nm",
            font=("SF Mono", 14),
            bg="#161b22",
            fg="#c9d1d9",
        )
        self.peak_label.pack(side=tk.LEFT, padx=24)

        self.power_label = tk.Label(
            stats_bar,
            text="Power: 1.00σT⁴",
            font=("SF Mono", 14),
            bg="#161b22",
            fg="#c9d1d9",
        )
        self.power_label.pack(side=tk.LEFT, padx=24)

        # Color display
        color_display = tk.Frame(right_panel, bg="#0d1117")
        color_display.pack(pady=(20, 0))

        color_container = tk.Frame(color_display, bg="#21262d", padx=4, pady=4)
        color_container.pack()

        self.color_canvas = tk.Canvas(
            color_container, width=80, height=80, bg="#0d1117", highlightthickness=0
        )
        self.color_canvas.pack()
        self.color_canvas.create_oval(
            4, 4, 76, 76, fill="#c9a227", outline="#30363d", width=2
        )

        tk.Label(
            color_display,
            text="Apparent Color",
            font=("SF Pro Text", 10),
            bg="#0d1117",
            fg="#484f58",
        ).pack(pady=(4, 0))

        # Spectrum plot
        plot_frame = tk.Frame(right_panel, bg="#0d1117")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.figure = Figure(figsize=(9, 4.5), facecolor="#0d1117")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#0d1117")
        self.ax.spines["bottom"].set_color("#30363d")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["left"].set_color("#30363d")
        self.ax.spines["right"].set_visible(False)
        self.ax.tick_params(colors="#8b949e", labelsize=9)
        self.ax.set_xlabel("Wavelength (nm)", color="#8b949e", fontsize=10)
        self.ax.set_ylabel(
            "Spectral Radiance (normalized)", color="#8b949e", fontsize=10
        )
        self.ax.set_xlim(100, 1600)
        self.ax.set_ylim(0, 1.15)

        # Visible spectrum band
        self.ax.axvspan(VISIBLE_MIN, VISIBLE_MAX, alpha=0.08, color="#ffffff")

        # Rainbow gradient background
        x_grad = np.linspace(VISIBLE_MIN, VISIBLE_MAX, 200)
        for i in range(len(x_grad) - 1):
            r, g, b = wavelength_to_rgb((x_grad[i] + x_grad[i + 1]) / 2)
            self.ax.axvspan(x_grad[i], x_grad[i + 1], alpha=0.25, color=(r, g, b))

        # Labels
        self.ax.text(230, 0.95, "IR", color="#484f58", fontsize=10, ha="center")
        self.ax.text(
            580, 0.95, "Visible Spectrum", color="#8b949e", fontsize=10, ha="center"
        )
        self.ax.text(1200, 0.95, "UV", color="#484f58", fontsize=10, ha="center")

        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        (self.spectrum_line,) = self.ax.plot([], [], color="#e94560", linewidth=2.5)
        (self.glow_line,) = self.ax.plot(
            [], [], color="#e94560", linewidth=10, alpha=0.15
        )

    def on_temp_change(self, val):
        self.temperature = int(float(val))
        self.temp_value_label.config(text=f"{self.temperature:,} K")
        self.update_simulation()

    def set_temperature(self, temp):
        self.temp_var.set(temp)
        self.temperature = temp
        self.temp_value_label.config(text=f"{self.temperature:,} K")
        self.update_simulation()

    def update_simulation(self):
        wavelengths = np.linspace(100, 1600, 800)
        intensities = planck_law(wavelengths, self.temperature)
        intensities_norm = (
            intensities / np.max(intensities)
            if np.max(intensities) > 0
            else intensities
        )

        self.spectrum_line.set_data(wavelengths, intensities_norm)
        glow_intensity = intensities_norm * (0.4 + 0.2 * np.sin(self.animation_phase))
        self.glow_line.set_data(wavelengths, glow_intensity)

        r, g, b = get_blackbody_color(self.temperature)
        hex_color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

        self.color_canvas.delete("all")
        self.color_canvas.create_oval(
            4, 4, 76, 76, fill=hex_color, outline="#30363d", width=2
        )

        lambda_max = b_wien / self.temperature * 1e9
        self.peak_label.config(text=f"λ_max: {lambda_max:.0f} nm")

        relative_power = (self.temperature / 5000) ** 4
        self.power_label.config(text=f"Power: {relative_power:.2f}σT⁴")

        self.figure.canvas.draw()

    def run_animation(self):
        self.animation_phase += 0.04
        self.update_simulation()
        self.root.after(16, self.run_animation)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackBodySimulator(root)
    root.mainloop()
