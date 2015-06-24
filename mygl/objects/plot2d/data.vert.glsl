/**
 * renders a given vertex and
 * passes geometry_color to geometry shader
 * XXX variable geometry_color
 */
#version 410

in vec4 vertex_position;
out vec2 geometry_point_value;

uniform float dot_size;
uniform mat4 mat_plane;
uniform mat4 mat_modelview;
uniform float time;
vec4 kernel_result;
int i;
vec2 f(vec2 x){return vec2(x.x, 0);}

void main() {

    kernel_result = f(vertex_position);
    geometry_point_value.xy = vec2(kernel_result.z, kernel_result.w);
    //vertex_position.y = 1.0;
    gl_Position = mat_plane*vec4(kernel_result.xy, 0.0, 1.0);
    gl_Position.x += dot_size;
    gl_Position.y += dot_size;
    gl_Position = mat_modelview*gl_Position;
}
