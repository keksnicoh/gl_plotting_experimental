/**
 * renders a simple fragment by assigning
 * given input fragment_color to output_color
 */
#version 410
in vec4 fragment_color;
out vec4 output_color;
void main()
{
    output_color = fragment_color;
}
