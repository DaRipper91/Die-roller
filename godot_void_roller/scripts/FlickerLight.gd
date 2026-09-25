extends OmniLight3D

@export var min_energy: float = 0.5
@export var max_energy: float = 2.5
@export var flicker_speed: float = 0.1

var target_energy: float = 2.0
var time_passed: float = 0.0

func _process(delta: float):
    light_color = GameManager.get_rainbow_color()
    time_passed += delta
    if time_passed >= flicker_speed:
        time_passed = 0
        target_energy = randf_range(min_energy, max_energy)
        # Occasionally dip very low for a "pop" effect
        if randf() < 0.1:
            target_energy = 0.1
            flicker_speed = 0.05
        else:
            flicker_speed = randf_range(0.05, 0.3)
    
    light_energy = lerp(light_energy, target_energy, delta * 15.0)
