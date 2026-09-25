shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;
uniform float scanline_count = 320.0;
uniform float scanline_opacity = 0.2;
uniform float vignette_opacity = 0.3;
uniform float brightness = 1.0;
uniform float noise_amount = 0.04;
uniform float signal_interference = 0.05;
uniform float aberration = 0.002;
uniform float bloom_intensity = 0.4;

float noise(vec2 uv) {
    return fract(sin(dot(uv.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

void fragment() {
    vec2 uv = SCREEN_UV;
    
    // FLAT SCREEN - No curvature logic here.
    
    // 1. Horizontal Signal Jitter (Much subtler)
    float jitter = (noise(vec2(TIME * 2.0, uv.y)) - 0.5) * signal_interference * 0.005;
    uv.x += jitter;
    
    // 2. Chromatic Aberration
    float r = texture(screen_texture, uv + vec2(aberration, 0.0)).r;
    float g = texture(screen_texture, uv).g;
    float b = texture(screen_texture, uv - vec2(aberration, 0.0)).b;
    vec4 color = vec4(r, g, b, 1.0);
    
    // 3. Fake Bloom
    vec4 blur = texture(screen_texture, uv + vec2(0.0015, 0.0015)) + 
                texture(screen_texture, uv - vec2(0.0015, 0.0015));
    color += blur * 0.08 * bloom_intensity;
    
    // 4. Clean Scanlines
    float scanline = sin(uv.y * scanline_count * PI * 2.0);
    color.rgb -= scanline * scanline_opacity * color.rgb;
    
    // 5. Vignette (Dark edges)
    vec2 centered_uv = uv * 2.0 - 1.0;
    float vignette = 1.0 - length(centered_uv) * vignette_opacity;
    color.rgb *= vignette;
    
    // 6. Subtle Static
    color.rgb += (noise(uv + TIME) - 0.5) * noise_amount;
    
    color.rgb *= brightness;
    COLOR = color;
}
