#version 410
uniform mat4 mat_projection;
uniform mat4 mat_modelview;
in vec3 vertex_position;
void main()
{
    gl_Position = mat_projection * mat_modelview * vec4(vertex_position, 1.0);
}
