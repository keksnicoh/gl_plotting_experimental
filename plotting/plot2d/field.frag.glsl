#version 410

uniform vec4 color;
uniform mat3 mat_domain;
uniform mat4 mat_modelview;
uniform float t;
out vec4 fragment_color;

bool float_eq_eps(float a, float b) {
    if (a < (b+0.1) && a > (b-0.1)) {
        return true;
    }
    return false;
}
bool vec2_eq_eps(vec2 a, vec2 b) {
    vec2 d = vec2(a.x-b.x,a.y-b.y);
    if (sqrt(d.x*d.x+d.y*d.y) < 0.05) {
        return true;
    }
    return false;
}

vec4 f(vec2 pc) { return vec4(0, 0, 0, 1); }
void main()
{
    vec2 pc = (mat_domain*vec3(gl_PointCoord.xy , 1)).xy;
    fragment_color = clamp(f(pc), 0.0, 1.0);
    return;
}
