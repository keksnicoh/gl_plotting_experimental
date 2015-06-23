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

void main() {
    // data2[3*x+2] = math.sin(math.sqrt(data2[3*x+0]**2+data2[3*x+1]**2)*50-(time()+start_time)*10)
    // data2[3*x+2] += math.sin(math.sqrt((data2[3*x+0]-0.05)**2+(data2[3*x+1]+0.0)**2)*50-(time()+start_time)*10)
    // data2[3*x+2] += math.sin(math.sqrt((data2[3*x+0]+0.05)**2+(data2[3*x+1]-0.0)**2)*50-(time()+start_time)*10)
    geometry_point_value.x = 0.0;
    for (i=0;i < 50;i+=1) {
        geometry_point_value.x += sin(-time*5+50*sqrt(
            pow(vertex_position.x   + 0.5 - i*0.02,2)
            + pow(vertex_position.y + 0.0,2)));
    }
    geometry_point_value.y = vertex_position.w;

    geometry_point_value.x = geometry_point_value.x / 10;
    gl_Position = mat_modelview*mat_plane*vec4(
        vertex_position.x+dot_size/2, // put vertex in center of
        vertex_position.y+dot_size/2, // the quad rendered by geom shader
        0.0,
        1.0
    );
}
