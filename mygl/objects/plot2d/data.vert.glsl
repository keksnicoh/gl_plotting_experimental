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
int i;
vec2 f(vec2 x){return vec2(x.x, 0);}

void main() {

    geometry_point_value = f(vertex_position.xy);

    gl_Position = mat_plane*vec4(vertex_position.xy, 0.0, 1.0);
    gl_Position.x += dot_size;
    gl_Position.y += dot_size;
    gl_Position = mat_modelview*gl_Position;
}
