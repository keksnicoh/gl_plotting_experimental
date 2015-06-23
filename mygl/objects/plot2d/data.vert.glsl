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

void main() {
    geometry_point_value = vec2(
        vertex_position.z,
        vertex_position.w
    );
    gl_Position = mat_modelview*mat_plane*vec4(
        vertex_position.x+dot_size/2, // put vertex in center of
        vertex_position.y+dot_size/2, // the quad rendered by geom shader
        0.0,
        1.0
    );
}
