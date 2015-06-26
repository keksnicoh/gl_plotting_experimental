/**
 * simple shader performs transformation matricies
 * on verticies and passes vertex_color to fragment_shader
 */
#version 410
in vec2 vertex_position;
in vec4 vertex_color;
out vec4 fragment_color;
uniform mat4 mat_plane;
uniform mat4 mat_modelview;
uniform float dot_size;
void main() {

    fragment_color = vertex_color;
    gl_Position = mat_modelview*mat_plane*vec4(vertex_position, 0.0, 1.0);
}
