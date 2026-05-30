extends Label

@export var speed: float = 0.05
var full_text: String = ""
var current_text: String = ""

func _ready():
	full_text = text
	text = ""
	start_typewriter()

func start_typewriter():
	text = ""
	for i in range(full_text.length()):
		text += full_text[i]
		# Play a small click sound here if we had one
		await get_tree().create_timer(speed).timeout

func set_new_text(new_text: String):
	full_text = new_text
	start_typewriter()
