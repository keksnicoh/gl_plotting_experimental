from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain
from functools import partial

KERNEL = """

float g(float r, float x) {
    return r*x*(1-x);
}

vec4 f(vec4 x) {
    float x0 = x.y;
    float x1;
    for (int i = 0; i < min(100, int(10*time)); i+=1) {
        x0 = g(x.x, x0);
    }
    return vec4(x.x, x0, 1, .02);
}


"""
domain = cartesian_domain(4000, 1.0, 1.99, origin=(-3.0,0.01))

plotter_app(KERNEL, (domain[0], partial(max, 0.0018)), origin=(-3,0), axis=(1.0,1.0))
