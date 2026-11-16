# Die-roller (Void Roller) Agent Guide & Invariants

Void Roller is a horror-themed multiplayer tabletop dice simulator with three target runtimes:
1. **Terminal Python Engine** (`die_roller.py`): ANSI/VT100 escape codes, ANSI color corruption, sanity degradation mechanics, and particle system.
2. **Terminal C++ Native Engine** (`die_roller.cpp`): High-performance POSIX terminal implementation (`g++ -O2 -o die_roller die_roller.cpp -lpthread`).
3. **Godot 4 HD Engine** (`godot_void_roller/`): 3D physics-based dice roller with CRT shaders and amber horror aesthetic.

## Architecture & Aesthetics
- **Aesthetic:** High-contrast amber (`#ff8100` / ANSI 220) on void black, terminal glitching, subliminal messages, and corruption-driven sanity collapse.
- **Single Source of Truth:** `AGENTS.md` is canonical; `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` are symlinks pointing directly to it.

## Verification Commands
```bash
# Run automated regression tests
pytest tests/

# Compile C++ terminal binary
g++ -O2 -o die_roller die_roller.cpp -lpthread

# Run terminal Python version
python3 die_roller.py
```
