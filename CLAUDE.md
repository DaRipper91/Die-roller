# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Void Roller** is a horror-themed multiplayer dice game with two implementations:

1. **Terminal versions** (`die_roller.py`, `die_roller.cpp`) — standalone ASCII/ANSI scripts that run in a terminal emulator (ideally `cool-retro-term`).
2. **Godot HD version** (`godot_void_roller/`) — the primary, actively developed implementation using Godot 4.x with 3D physics dice, CRT shaders, and the full horror aesthetic.

The aesthetic is "Daripper amber horror": high-contrast amber (`#ff8100` / color code 220), dark void backgrounds, leet-speak messages, and escalating horror effects tied to a corruption system.

## Commands

### Running the Game

```bash
# Launch Godot HD version (preferred)
./launch_void.sh
# or directly:
godot --path godot_void_roller --fullscreen

# Launch terminal Python version
python3 die_roller.py
python3 die_roller.py --scare   # Start at corruption level 5

# Build and run C++ terminal version
g++ -o die_roller die_roller.cpp -lpthread && ./die_roller
```

### Godot Editor

```bash
# Open project in Godot editor
godot --path godot_void_roller --editor

# Headless test run (if tests are added)
godot --path godot_void_roller --headless --run-tests
```

## Architecture

### Godot HD Version (`godot_void_roller/`)

The Godot project uses **Forward Plus renderer** at 1280×720 with a custom amber/dark theme.

**Scene tree:**
- `scenes/Main.tscn` — root scene; contains the full UI overlay and the 3D dice viewport
  - `DiceViewportContainer/SubViewport/DiceScene` — isolated 3D environment for dice physics
  - `UI/` — all 2D UI panels (name entry, top bar, blight selection, cursed overlay)
- `scenes/Die3D.tscn` — `RigidBody3D` die; instantiated at runtime into `DiceScene`
- `scenes/DiceRoom.tscn` — `StaticBody3D` walls/floor that contain the rolling dice

**Scripts:**
- `scripts/GameManager.gd` — **autoload singleton**. Owns all game state: `players[]`, `player_data{}` (corruption + sanity per player), turn index. Emits signals (`turn_started`, `corruption_changed`, `sanity_changed`) that `Main.gd` listens to.
- `scripts/Main.gd` — UI controller. Handles input (`_process`), rolls dice by instantiating `Die3D` scenes, reads final values after physics settle, triggers horror overlays, and routes blight selection.
- `scripts/Die3D.gd` — physics die. `get_die_value()` determines the face-up value by dotting each local axis against `Vector3.UP`. `val` is set to a non-zero glitch value to force-override the physics result (used for Cursed 13 rolls).
- `scripts/TypewriterLabel.gd` — utility for the typewriter text effect.

**Shaders** (`shaders/`):
- `crt_shader.gdshader` — full-screen post-process (scanlines, chromatic aberration, fake bloom, vignette, static). Applied to the top-level `ColorRect` covering the viewport.
- `panel_scanlines.gdshader` — lighter scanline pass for UI panels.
- `ps1_jitter.gdshader` — vertex jitter for the PS1 retro dice look (planned/in-progress).

### Core Game Logic (shared across all versions)

**Corruption system:**
- Each player has a `corruption` level starting at 0.
- Rolling **7 or 11** triggers a "Blighted Gift": the active player chooses who gains +1 corruption.
- Rolling **13** (Cursed 13) triggers the hijack sequence and grants the roller −2 corruption.
- Sanity labels derive from corruption: 0=STABLE, 1-2=SHAKEN, 3-5=HEARING VOICES, 6-8=FRACTURED, 9+=LOST TO THE VOID.

**Cursed 13 mechanic:**
- In Godot, `roll_dice()` computes `is_cursed = randf() < 0.03 + (corruption * 0.01)`. If cursed, `f1+f2=13` is forced by setting `current_dice[i].val` after physics settle.
- In Python, `Die` supports face values 7, 8, and 13 (impossible on a real die) as glitch states.

### Terminal Versions

Both `die_roller.py` and `die_roller.cpp` are self-contained single-file programs:
- They share the same color codes, effect names (`effect_static`, `effect_glitch`, `effect_melt`, `effect_system_breach`, `effect_singularity`), and corruption thresholds.
- The Python version is more feature-complete: multiplayer, `--scare` flag, audio via `aplay`, player-name-aware whisper messages, and `Particle`/`Die` physics classes for terminal animation.
- The C++ version is single-player only with a background `stalker_loop` thread.

## Development Notes

- The Godot project targets **Godot 4.6** (Forward Plus renderer). Do not use Godot 3.x APIs.
- `GameManager` is registered as an autoload in `project.godot` — access it globally without `get_node`.
- Die face value detection in `Die3D.gd` uses dot products against `Vector3.UP`; the face map is `{+Y:1, -Y:6, +X:2, -X:5, +Z:3, -Z:4}`.
- The "Cursed 13" forced roll sets `die.val` on the `Die3D` instance *after* physics settle, then `get_die_value()` returns that override if it differs from the physics result.
- Phases 3–5 from `godot_plan.md` are still in progress: blight effect sequences, subliminal flash, audio, and the full Cursed 13 hijack animation are partially implemented or stubbed.
