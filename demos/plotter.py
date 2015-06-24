from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain, x_axis_domain

if __name__ == '__main__':
    KERNEL = """
    float c;
    float tx;
    float ty;
    vec4 f(vec4 x) {
        c = 0.0;
        for (i=0;i < 50;i+=1) {
            tx = x.x + 0.5 -0.02*i;
            ty = x.y - 0.1 + 0.001*i;
            c += sin(50*sqrt(tx*tx + ty*ty)-5*time);
        }
        return vec4(x.xy, c / 7, vertex_position.w);
    }
    """


    KERNEL_SIN = """
    vec4 f(vec4 x) {
        x.y = 1.0;
        return vec4(x.x, sin(x.x), 1,0);
    }
    """
    #plotter_app(KERNEL, cartesian_domain(200, 3.0, 3.0))
    plotter_app(KERNEL_SIN, x_axis_domain(500, 3.0))
