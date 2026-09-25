extends Label

func _process(_delta):
	add_theme_color_override("font_color", GameManager.get_rainbow_color())
