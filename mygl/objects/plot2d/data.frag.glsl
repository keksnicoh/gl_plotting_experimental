#version 410
in vec4 fragment_color;
in vec2 fragment_point_value;
out vec4 output_color;

vec4 point_color(vec2 value, vec4 fragment_color) {
    return vec4(
        fragment_color.x*value.x,
        fragment_color.y*value.x,
        fragment_color.z*value.x,
        fragment_color.w*value.y
    );
}

void main()
{
    if (fragment_point_value[1] == 0) {
        discard;
    }
    output_color = point_color(fragment_point_value, fragment_color);
}
