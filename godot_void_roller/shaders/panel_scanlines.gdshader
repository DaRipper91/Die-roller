shader_type canvas_item;

uniform vec4 base_color : source_color = vec4(0.0, 0.0, 0.0, 0.8);
uniform float scanline_density = 50.0;
uniform float scanline_opacity = 0.2;

void fragment() {
	vec4 col = base_color;
	float s = sin(UV.y * scanline_density * PI * 2.0);
	col.rgb -= s * scanline_opacity;
	COLOR = col;
}
