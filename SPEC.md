# Black Body Radiation Simulation

## Project Overview
- **Project name**: Black Body Simulator
- **Type**: Interactive GUI application with animation
- **Core functionality**: Simulate black body radiation based on Planck's law with animated visualization of the spectrum and color temperature relationship
- **Target users**: Physics students, educators, and enthusiasts

## Visual & Rendering Specification

### Scene Setup
- **Display**: 2D spectral plot with wavelength on x-axis, intensity on y-axis
- **Background**: Dark GitHub-style theme (#0d1117) for accurate color representation
- **Layout**: Control panel on left (280px), spectrum display on right

### Color Palette
- **Background**: #0d1117 (deep dark)
- **Panels**: #161b22 (dark gray)
- **Cards/Buttons**: #21262d (medium gray)
- **Accent**: #e94560 (coral red)
- **Text primary**: #f0f6fc (off-white)
- **Text secondary**: #8b949e (muted gray)

### Typography
- System fonts (SF Pro style on Linux) for clean modern look
- Temperature display: 36px bold
- Section headers: 10px bold uppercase
- Stats: 14px monospace

### Materials & Effects
- **Spectrum rendering**: Full visible spectrum (380-780nm) with rainbow gradient background
- **Color display**: Actual black body color for given temperature
- **Glow effect**: Animated "pulsing" glow on spectrum curve representing radiated power
- **Visible band**: Highlighted visible spectrum region on graph

## Simulation Specification

### Physics Model
- **Planck's law**: B(λ,T) = (2hc²/λ⁵) × 1/(e^(hc/λkT) - 1)
- **Wien's displacement law**: λ_max = b/T where b = 2.898×10⁻³ m·K
- **Stefan-Boltzmann law**: E = σT⁴

### Parameters
- **Temperature range**: 1000K to 30000K (adjustable via slider)
- **Default temperature**: 5000K (sun-like)
- **Wavelength range**: 100nm to 1600nm (covers IR to UV)

### Animation
- **Animated spectrum curve**: Smooth transitions when temperature changes
- **Pulsing glow**: Rate based on animation speed setting
- **Color interpolation**: Smooth color transition as temperature changes

## Interaction Specification

### Controls
- **Temperature slider**: 1000K - 30000K range with horizontal scale
- **Preset buttons**: 5 color-coded presets in a grid layout
  - Iron (1000K) - dark red
  - Candle (3000K) - orange
  - Sun (5000K) - yellow
  - Daylight (6500K) - white
  - Blue Star (10000K) - light blue
- **Play/Pause button**: Toggle animation
- **Speed control**: Animation speed slider (0.2x to 3.0x)

### Display Outputs
- **Temperature value**: Displayed with comma separator and "K" suffix
- **Wien's λ_max**: Peak wavelength in nanometers
- **Radiated power**: Relative intensity (σT⁴ normalized to 5000K reference)
- **Apparent color**: Colored circle showing perceived black body color
- **Spectrum graph**: Planck curve with rainbow gradient background, IR/Visible/UV regions labeled

## Acceptance Criteria
1. Application launches with dark modern UI
2. Temperature slider smoothly adjusts temperature from 1000K to 30000K
3. Spectrum curve accurately follows Planck's law
4. Color circle shows correct black body color for temperature
5. Animation runs smoothly at ~60fps
6. Preset buttons instantly set correct temperatures
7. All labels and values update in real-time
8. Rainbow gradient visible spectrum background displays correctly