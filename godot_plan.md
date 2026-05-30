# Godot "Void Roller" Implementation Plan

## Overview
Migrating the terminal-based "Void Roller" to a high-fidelity Godot 4 project. We're moving from ASCII blocks to 3D dice, custom shaders, and immersive audio while keeping the "Daripper" amber/horror aesthetic.

## Scope Definition
### In Scope
- 3D Physics-based dice rolling (2 dice).
- Multiplayer turn management (Name entry screen).
- Corruption & Sanity system logic.
- Horror effects: CRT Shader, Glitch Shaders, Subliminal Flashes.
- "Blight a Friend" choice mechanic.
- The "Cursed 13" anomaly (Impossible rolls/Hijack sequence).
- Glitchy audio feedback.

### Out of Scope
- Networked multiplayer (Local/Pass-and-play only).
- VR support.
- Microtransactions (The Void doesn't accept credit cards).

## Implementation Phases

### Phase 1: Project Scaffolding & Main UI (COMPLETED)
- Establishing the base Godot project and the retro-terminal UI layout.

### Phase 2: The Dice Room & Physics (REFINING)
- Goal: Real-time 3D dice physics in a contained terminal environment.
- [x] Set up a SubViewport for 3D content.
- [x] Create a "Dice Box" with StaticBody3D walls/floor.
- [x] Implement a Die3D (RigidBody3D).
- [ ] **UPGRADE**: Implement **PS1-style Vertex Jitter** shader for the dice to make them look shaky and retro.
- [ ] **UPGRADE**: Use a high-poly-to-low-poly baked dice model or a custom mesh with high-contrast amber pip textures.

### Phase 3: Corruption & Sanity Engine (IN PROGRESS)
- [x] GameManager autoload script.
- [x] Player data structures (Name, Corruption, Sanity).
- [ ] Port logic for 7/11 triggers and the "Blight Choice" UI popup.
- [ ] Implement Sanity label updates based on Corruption levels.

### Phase 4: The "Cursed" Aesthetic (UPGRADED)
- **Goal**: Recreate a "Haunted Security Monitor" look.
- [ ] **NEW**: Implement **Volumetric Fog** and a single flicker-heavy **OmniLight3D** for a dark room vibe.
- [ ] **NEW**: Upgrade CRT shader with **Signal Interference** (Antenna noise) and **Chromatic Aberration**.
- [ ] Implement the Subliminal Flash effect using a dedicated ColorRect and AnimationPlayer.
- [ ] Set up AudioStreamPlayer nodes for glitch sounds.

### Phase 5: The Cursed 13 (THE ANOMALY)
...
- **Goal**: Implement the rules-breaking anomaly.
- **Steps**:
  1. [ ] Add a `7` and `8` face to the `Die3D` mesh (glitched faces).
  2. [ ] Implement a chance-based trigger to "force" physics results toward a sum of 13.
  3. [ ] Build the `Hijack` animation (Screen-filling "13" sprites, maximum shader distortion).
  4. [ ] Implement the Corruption -2 reward for surviving.
- **Verification**: Force a 13 roll via debug key; verify the "Possession" sequence plays and corruption decreases.

## Verification Command
- `godot --path godot_void_roller --headless --run-tests` (if tests implemented) or manual verification of the "Daripper" look.
