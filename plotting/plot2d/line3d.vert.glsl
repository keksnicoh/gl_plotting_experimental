/**
 * renders a given vertex and
 * passes geometry_color to geometry shader
 * XXX variable geometry_color
 */
#version 410

uniform float dot_size;
uniform mat4 mat_projection;
uniform mat4 mat_modelview;

in vec4 vertex_position;
out vec2 fragment_point_value;

vec4 kernel_result;
vec4 f(vec4 x){return vec4(x.xyz, 1);}

void main() {
    kernel_result = f(vertex_position);
    fragment_point_value.xy = vec2(kernel_result.z, kernel_result.w);
    gl_Position = mat_projection*mat_modelview*vec4(kernel_result.xyz, 1.0);
    gl_Position = gl_Position;
}
