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
        return vec4(x.x, sin(exp(-x.x*x.x)*time), 1,0);
    }
    """

    KERNEL_LJAPUNOW_EXP = """
    vec4 f(vec4 x) {
        int iterations = 10000;
        float x_0 = 0.3;

        float y = 0;
        float summe = 0;
        for (int i=0; i < iterations - 1; i++) {
            y = x.x*cos(y);
            summe += log(abs(y));
        }
        x.y = 1.0;
        return vec4(x.x, (1.0/iterations)*summe, 1,0);
    }
    """

    #plotter_app(KERNEL, cartesian_domain(200, 3.0, 3.0))
    plotter_app(KERNEL_LJAPUNOW_EXP, x_axis_domain(50000, 4.0), origin=(0, 1), axis=(4.0,2.0))
    #plotter_app(KERNEL_SIN, x_axis_domain(100000, 3.0))
