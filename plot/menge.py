from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain, x_axis_domain

# plot all for a given condition
KERNEL_SIN = """
vec4 f(vec4 x) {
    int is_in = 0;
    if (x.x > -0.5 && x.y > -1.0 && sin(5*x.x*x.y) > 0) {
        is_in = 1;
    }

    return vec4(x.xy, sin(x.x*x.x+x.y*x.y*time), is_in);
}
"""
plotter_app(
    KERNEL_SIN,
    cartesian_domain(1000, 3.0, 3.0, origin=(1.5, 1.5)),
    axis=(3.0,3.0),
    origin=(1.5,1.5))
