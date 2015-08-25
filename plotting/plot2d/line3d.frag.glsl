#version 410
uniform vec4 color_min;
uniform vec4 color_max;

in vec2 fragment_point_value;
out vec4 output_color;

void main()
{
    vec4 color = mix(color_min, color_max, fragment_point_value.y);
    //color.w = color.w*fragment_point_value.y;

    output_color = color;
}
