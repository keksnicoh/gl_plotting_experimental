from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain, x_axis_domain

KERNEL_SIN = """
vec4 f(vec4 x) {
    x.y = 1.0;
    return vec4(x.x, x.x*sin(time*x.x)*sin(20*exp(-x.x*x.x)*time), 1,1);
}
"""
plotter_app(
    KERNEL_SIN,
    x_axis_domain(100000, 3.0, x_0=-1.5),
    axis=(3.0,3.0),
    origin=(1.5,1.5))
