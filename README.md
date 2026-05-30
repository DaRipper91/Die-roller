# Void Roller (HD)

A horror-themed multiplayer 3D dice roller for the terminal.

## Features
- **Godot 4 HD Graphics**: Real-time 3D dice with physics, volumetric lighting, and glowing pip labels.
- **Multiplayer Turn-Based Play**: Track individual corruption and sanity levels.
- **Horror Aesthetic**: High-contrast Amber (#ff8100) theme with retro-terminal UI.
- **The Cursed 13**: A rules-breaking anomaly that triggers reality-warping glitches.

## Requirements
- Godot Engine 4.x
- Linux (optimized for Fedora/cool-retro-term)

## How to Play
1. Launch the game using `./launch_void.sh`.
2. Enter player names (leave empty to start).
3. Press **Enter** or **Space** to roll the dice.
4. If you roll a **7** or **11**, you trigger a "Blighted Gift" and must choose who to corrupt.
5. Survive the void. Don't roll a **13**.

## Technical Details
- **Engine**: Godot 4.6 (Forward Plus renderer)
- **Shaders**: Flat-screen terminal effects with scanlines and aberration.
- **Fonts**: IBM 3270 Monospace.
- **Physics**: RigidBody3D dice with custom impulse logic.

## Controls
- **Enter/Space**: Roll Dice / Confirm Name.
- **Q**: Quit Game.
