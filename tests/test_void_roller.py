import os
import sys
import pytest

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import die_roller

def test_color_formatting():
    assert die_roller.get_color(220) == "\033[38;5;220m"
    assert die_roller.get_bg(232) == "\033[48;5;232m"

def test_sanity_status_levels():
    assert die_roller.get_sanity_status(0) == "STABLE"
    assert die_roller.get_sanity_status(1) == "SHAKEN"
    assert die_roller.get_sanity_status(2) == "SHAKEN"
    assert die_roller.get_sanity_status(3) == "HEARING VOICES"
    assert die_roller.get_sanity_status(5) == "HEARING VOICES"
    assert die_roller.get_sanity_status(7) == "FRACTURED"
    assert die_roller.get_sanity_status(9) == "LOST TO THE VOID"
    assert die_roller.get_sanity_status(99) == "LOST TO THE VOID"

def test_particle_class():
    p = die_roller.Particle(10, 20, 220)
    assert p.x == 10
    assert p.y == 20
    assert p.color == 220
    assert p.life > 0

def test_die_class():
    d = die_roller.Die(10, 10, 1.0, 1.0)
    assert d.val in range(1, 7)
    art = d.get_art()
    assert len(art) == 6
    orig_x = d.x
    d.update(80, 24)
    assert d.x != orig_x or d.vx == 0

def test_cpp_binary_built():
    bin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "die_roller")
    assert os.path.exists(bin_path)
    assert os.access(bin_path, os.X_OK)

def test_godot_project_exists():
    godot_proj = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "godot_void_roller", "project.godot")
    assert os.path.exists(godot_proj)
