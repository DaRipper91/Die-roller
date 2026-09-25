extends Node

signal turn_started(player_name)
signal turn_ended(player_name, dice_total)
signal corruption_changed(player_name, new_level)
signal sanity_changed(player_name, new_sanity)

var players = []
var player_data = {} # { "NAME": { "corruption": 0, "sanity": "STABLE" } }
var current_player_index = 0

func get_rainbow_color(offset: float = 0.0) -> Color:
	var t = (Time.get_ticks_msec() / 1000.0) + offset
	return Color.from_hsv(fmod(t * 0.5, 1.0), 0.8, 1.0)

func add_player(name: String):
	name = name.to_upper()
	if not player_data.has(name):
		players.append(name)
		player_data[name] = {
			"corruption": 0,
			"sanity": "STABLE"
		}

func get_current_player():
	if players.is_empty(): return ""
	return players[current_player_index]

func next_turn():
	current_player_index = (current_player_index + 1) % players.size()
	turn_started.emit(get_current_player())

func update_corruption(player_name: String, delta: int):
	if player_data.has(player_name):
		player_data[player_name]["corruption"] += delta
		var level = player_data[player_name]["corruption"]
		player_data[player_name]["sanity"] = get_sanity_status(level)
		corruption_changed.emit(player_name, level)
		sanity_changed.emit(player_name, player_data[player_name]["sanity"])

func get_sanity_status(level: int) -> String:
	if level == 0: return "STABLE"
	if level < 3: return "SHAKEN"
	if level < 6: return "HEARING VOICES"
	if level < 9: return "FRACTURED"
	return "LOST TO THE VOID"
