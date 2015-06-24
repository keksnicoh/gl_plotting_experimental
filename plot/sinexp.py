from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain, x_axis_domain

KERNEL_SIN = """
vec4 f(vec4 x) {
    x.y = 1.0;
    return vec4(x.x, sin(20*exp(-x.x*x.x)*time), 1,0);
}
"""
plotter_app(KERNEL_SIN, x_axis_domain(100000, 3.0))
