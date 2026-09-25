shader_type spatial;

uniform vec4 albedo : source_color = vec4(1.0);
uniform sampler2D texture_albedo : source_color;
uniform float jitter : hint_range(0.0, 1.0) = 0.5;
uniform float resolution : hint_range(16.0, 1024.0) = 320.0;

void vertex() {
    // Basic vertex jitter to simulate low-precision PS1-style coordinates
    vec4 v = PROJECTION_MATRIX * MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
    vec3 v_ndc = v.xyz / v.w;
    
    // Snapping
    v_ndc.xy = floor(v_ndc.xy * resolution) / resolution;
    
    vec4 v_snapped = vec4(v_ndc * v.w, v.w);
    VERTEX = (INV_PROJECTION_MATRIX * v_snapped).xyz;
}

void fragment() {
    vec4 albedo_tex = texture(texture_albedo, UV);
    ALBEDO = albedo.rgb * albedo_tex.rgb;
}
