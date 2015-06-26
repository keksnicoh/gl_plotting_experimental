#version 410
uniform vec4 color_min;
uniform vec4 color_max;

in vec2 fragment_point_value;
out vec4 output_color;

void main()
{
    if (fragment_point_value[1] == 0) {
        discard;
    }
    vec4 color = mix(color_min, color_max, fragment_point_value.x);
    color.w = color.w*fragment_point_value.y;

    output_color = color;
}
