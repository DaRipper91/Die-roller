extends RigidBody3D

@onready var ray_up = $RayCastUp
@onready var ray_down = $RayCastDown
@onready var ray_left = $RayCastLeft
@onready var ray_right = $RayCastRight
@onready var ray_forward = $RayCastForward
@onready var ray_back = $RayCastBack

@onready var label_up = $Labels/Label_Up
@onready var label_down = $Labels/Label_Down
@onready var label_front = $Labels/Label_Front
@onready var label_back = $Labels/Label_Back
@onready var label_right = $Labels/Label_Right
@onready var label_left = $Labels/Label_Left

var val = 0 # Current internal value

func _process(_delta):
	var color = GameManager.get_rainbow_color()
	if val == 0:
		label_up.modulate = color
		label_down.modulate = color
		label_front.modulate = color
		label_back.modulate = color
		label_right.modulate = color
		label_left.modulate = color
	else:
		# If glitched, maybe strobe faster?
		label_up.modulate = GameManager.get_rainbow_color(1.0)
		label_down.modulate = GameManager.get_rainbow_color(1.0)
		label_front.modulate = GameManager.get_rainbow_color(1.0)
		label_back.modulate = GameManager.get_rainbow_color(1.0)
		label_right.modulate = GameManager.get_rainbow_color(1.0)
		label_left.modulate = GameManager.get_rainbow_color(1.0)

func get_die_value() -> int:
	# Standard die mapping (Simplified)
	# Ray Up colliding -> The Bottom face is on the floor, so Top face (Up) is the value.
	# Actually, in Godot, if RayUp hits the ceiling, that's not what we want.
	# We want to know which ray is pointing UP in global space.
	
	var rays = {
		ray_up: 1,
		ray_down: 6,
		ray_right: 2,
		ray_left: 5,
		ray_forward: 3,
		ray_back: 4
	}
	
	var max_dot = -1.0
	var best_val = 1
	
	# Check local axes against global UP
	var local_up = global_transform.basis.y
	var local_down = -global_transform.basis.y
	var local_right = global_transform.basis.x
	var local_left = -global_transform.basis.x
	var local_forward = global_transform.basis.z
	var local_back = -global_transform.basis.z
	
	var axes = {
		local_up: 1,
		local_down: 6,
		local_right: 2,
		local_left: 5,
		local_forward: 3,
		local_back: 4
	}
	
	for axis in axes:
		var dot = axis.dot(Vector3.UP)
		if dot > max_dot:
			max_dot = dot
			best_val = axes[axis]
			
	# If we have a forced glitch value, return that instead
	if val != 0 and val != best_val:
		_update_glitch_visuals(val)
		return val
		
	return best_val

func _update_glitch_visuals(glitch_val: int):
	# Update the label that is currently on top to show the glitch value
	var local_up = global_transform.basis.y
	var local_down = -global_transform.basis.y
	var local_right = global_transform.basis.x
	var local_left = -global_transform.basis.x
	var local_forward = global_transform.basis.z
	var local_back = -global_transform.basis.z
	
	var labels = {
		local_up: label_up,
		local_down: label_down,
		local_right: label_right,
		local_left: label_left,
		local_forward: label_front,
		local_back: label_back
	}
	
	var max_dot = -1.0
	var top_label = label_up
	for axis in labels:
		var dot = axis.dot(Vector3.UP)
		if dot > max_dot:
			max_dot = dot
			top_label = labels[axis]
	
	top_label.text = str(glitch_val)

func roll(impulse: Vector3, torque: Vector3):
	val = 0 # Reset glitch
	# Reset label text if they were glitched
	label_up.text = "1"
	label_down.text = "6"
	label_front.text = "3"
	label_back.text = "4"
	label_right.text = "2"
	label_left.text = "5"
	
	apply_central_impulse(impulse)
	apply_torque_impulse(torque)
