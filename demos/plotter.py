from app.plot2d import plotter_app
from mygl.objects.plot2d import cartesian_domain

if __name__ == '__main__':
    KERNEL = """
    float c;
    float tx;
    float ty;
    vec2 f(vec2 x) {
        c = 0.0;
        for (i=0;i < 50;i+=1) {
            tx = x.x + 0.5 -0.02*i;
            ty = x.y - 0.1 + 0.001*i;
            c += sin(50*sqrt(tx*tx + ty*ty)-5*time);
        }
        return vec2(c / 7, vertex_position.w);
    }
    """
    plotter_app(KERNEL, cartesian_domain(200, 3.0, 3.0))
