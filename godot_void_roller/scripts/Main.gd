extends Control

@onready var name_entry_overlay = $UI/NameEntryOverlay
@onready var name_input = $UI/NameEntryOverlay/VBox/LineEdit
@onready var player_list_label = $UI/NameEntryOverlay/VBox/CurrentPlayers
@onready var top_player_label = $UI/TopBar/HBox/PlayerLabel
@onready var top_sanity_label = $UI/TopBar/HBox/SanityLabel
@onready var top_corruption_label = $UI/TopBar/HBox/CorruptionLabel

@onready var dice_scene = $DiceViewportContainer/SubViewport/DiceScene
@onready var blight_overlay = $UI/BlightOverlay
@onready var blight_buttons_container = $UI/BlightOverlay/VBox/PlayerButtons
@onready var result_label = $UI/ResultLabel
@onready var cursed_overlay = $UI/CursedOverlay
@onready var cursed_noise = $UI/CursedOverlay/Noise
@onready var cursed_message = $UI/CursedOverlay/Message

var die_scene = preload("res://scenes/Die3D.tscn")
var rolling = false
var current_dice = []

func _ready():
	GameManager.corruption_changed.connect(_on_corruption_changed)
	GameManager.sanity_changed.connect(_on_sanity_changed)
	GameManager.turn_started.connect(_on_turn_started)
	show_name_entry()

func show_name_entry():
	name_entry_overlay.show()
	name_input.grab_focus()
	_update_player_list_display()

func _update_player_list_display():
	if GameManager.players.is_empty():
		player_list_label.text = ""
	else:
		player_list_label.text = "(Current players: " + ", ".join(GameManager.players) + ")"

func _process(_delta):
	# Using Input singleton for most reliable key polling
	if name_entry_overlay.visible:
		if Input.is_action_just_pressed("ui_accept"):
			var player_name = name_input.text.strip_edges()
			if player_name == "":
				if GameManager.players.is_empty():
					GameManager.add_player(OS.get_environment("USER"))
				start_game()
			else:
				GameManager.add_player(player_name)
				name_input.clear()
				_update_player_list_display()
	elif not (blight_overlay.visible or cursed_overlay.visible):
		if Input.is_action_just_pressed("roll") or Input.is_action_just_pressed("ui_accept"):
			if not rolling:
				roll_dice()
		if Input.is_key_pressed(KEY_Q):
			get_tree().quit()

func roll_dice():
	rolling = true
	result_label.hide()
	for d in current_dice: d.queue_free()
	current_dice.clear()
	
	var corruption = GameManager.player_data[GameManager.get_current_player()]["corruption"]
	var is_cursed = randf() < 0.03 + (corruption * 0.01)
	var f1 = null
	var f2 = null
	if is_cursed:
		f1 = 7 if randf() > 0.5 else 6
		f2 = 13 - f1
	
	for i in range(2):
		var die = die_scene.instantiate()
		dice_scene.add_child(die)
		die.global_position = Vector3(randf_range(-1, 1), 6, randf_range(-1, 1))
		die.roll(
			Vector3(randf_range(-15, 15), randf_range(10, 20), randf_range(-15, 15)),
			Vector3(randf_range(-30, 30), randf_range(-30, 30), randf_range(-30, 30))
		)
		current_dice.append(die)
	
	await get_tree().create_timer(1.0).timeout
	var start_time = Time.get_ticks_msec()
	while (Time.get_ticks_msec() - start_time) < 6000:
		var all_stopped = true
		for d in current_dice:
			if d.linear_velocity.length() > 0.05 or d.angular_velocity.length() > 0.05:
				all_stopped = false
				break
		if all_stopped: break
		await get_tree().create_timer(0.1).timeout
	
	if is_cursed:
		current_dice[0].val = f1
		current_dice[1].val = f2

	var v1 = current_dice[0].get_die_value()
	var v2 = current_dice[1].get_die_value()
	var total = v1 + v2
	
	if total == 13:
		await trigger_cursed_13()
		GameManager.update_corruption(GameManager.get_current_player(), -2)
		finish_turn()
		return

	result_label.text = " ▞ " + str(v1) + " + " + str(v2) + " = " + str(total) + " ▚ "
	if total in [7, 11]:
		result_label.add_theme_color_override("font_color", Color(1, 0, 0))
	else:
		result_label.add_theme_color_override("font_color", Color(1, 0.5, 0))
	result_label.show()
	
	await get_tree().create_timer(2.0).timeout
	
	if total in [7, 11]:
		if GameManager.players.size() > 1:
			show_blight_selection()
			return
		else:
			GameManager.update_corruption(GameManager.get_current_player(), 1)
	
	finish_turn()

func trigger_cursed_13():
	cursed_overlay.show()
	var messages = [
		"Y0U W3R3 N3V3R 5UPP053D 70 R34CH 7H15",
		"7H3 D1C3 H4V3 N0 M34N1N6 H3R3",
		"7H3 V01D 15 N07 4 64M3",
		"6 0 0 D 8 Y 3"
	]
	for msg in messages:
		cursed_message.text = msg
		for i in range(15):
			var noise = ""
			for j in range(300): noise += "13 " if randf() > 0.5 else "   "
			cursed_noise.text = noise
			await get_tree().create_timer(0.04).timeout
	await get_tree().create_timer(1.0).timeout
	cursed_overlay.hide()

func show_blight_selection():
	blight_overlay.show()
	for child in blight_buttons_container.get_children(): child.queue_free()
	for i in range(GameManager.players.size()):
		var p_name = GameManager.players[i]
		var btn = Button.new()
		btn.text = "[" + str(i+1) + "] " + p_name + " (Level: " + str(GameManager.player_data[p_name]["corruption"]) + ")"
		btn.pressed.connect(_on_blight_target_selected.bind(p_name))
		blight_buttons_container.add_child(btn)
		if i == 0: btn.grab_focus()

func _on_blight_target_selected(target_name):
	blight_overlay.hide()
	GameManager.update_corruption(target_name, 1)
	finish_turn()

func finish_turn():
	rolling = false
	GameManager.next_turn()

func start_game():
	name_entry_overlay.hide()
	name_input.focus_mode = Control.FOCUS_NONE
	GameManager.turn_started.emit(GameManager.get_current_player())

func _on_turn_started(player_name):
	top_player_label.text = "▚ " + player_name + " ▞"
	var data = GameManager.player_data[player_name]
	top_sanity_label.text = "SANE_LEVEL: " + data["sanity"]
	top_corruption_label.text = "▚ CORRUPTION: " + str(data["corruption"]) + " ▞"

func _on_corruption_changed(player_name, level):
	if player_name == GameManager.get_current_player():
		top_corruption_label.text = "▚ CORRUPTION: " + str(level) + " ▞"

func _on_sanity_changed(player_name, sanity):
	if player_name == GameManager.get_current_player():
		top_sanity_label.text = "SANE_LEVEL: " + sanity
