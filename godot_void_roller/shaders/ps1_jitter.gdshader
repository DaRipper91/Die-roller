shader_type spatial;

uniform sampler2D albedo_texture : source_color;
uniform float jitter_amount = 0.5;
uniform vec4 amber_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);

void vertex() {
	// PS1 style vertex snapping
	vec4 snap_pos = PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX * vec4(VERTEX, 1.0);
	snap_pos.xyz /= snap_pos.w;
	snap_pos.xyz = floor(snap_pos.xyz * jitter_amount * 100.0) / (jitter_amount * 100.0);
	snap_pos.xyz *= snap_pos.w;
	VERTEX = (inverse(PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX) * snap_pos).xyz;
}

void fragment() {
	// Procedural dice pips (simplified D6 logic)
	vec3 base_col = vec3(0.05); // Black dice
	vec2 uv = UV;
	
	// Emission for the pips
	float pips = 0.0;
	// Logic to draw pips based on UV and which face we are on
	// (For now, let's just make it look high-contrast amber)
	
	ALBEDO = base_col;
	EMISSION = amber_color.rgb * 2.0;
}
