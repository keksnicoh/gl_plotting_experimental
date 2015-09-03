/**
 * renders a square around a given gl_Position.
 * also it passes the geometry_color[1] as fragment_color
 * to the fragment shader
 */
#version 410
layout (points) in;
layout (triangle_strip) out;
layout (max_vertices = 4) out;
in vec2 geometry_point_value[1];
out vec2 fragment_point_value;
uniform vec4 geometry_color;
uniform float dot_size_x;
uniform float dot_size_y;
out vec4 fragment_color;
void main(void)
{
    fragment_point_value = geometry_point_value[0];
    gl_Position = gl_in[0].gl_Position + vec4(-dot_size_x,-dot_size_y, 0, 0) ;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4(-dot_size_x,dot_size_y, 0,0) ;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4(dot_size_x,-dot_size_y, 0,0) ;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4(dot_size_x,dot_size_y, 0,0) ;
    EmitVertex();

    EndPrimitive();
}
