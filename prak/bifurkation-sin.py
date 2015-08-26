from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy
from numpy import sin
from OpenGL.GL import *

LOGISTISCH_MAP = """
uniform float r;
vec4 f(vec4 x) {
    return vec4(x.x, r*sin(x), 1.0, 1.0);
}
"""

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 1.0);
}
"""

KERNEL_SIN = "float g(float r, float x) {return r*sin(x);}\n"
KERNEL_SIN_DIFF = "float dg(float r, float x) {return r*cos(x);}\n"
LYAPUNOV_NORMIERT = KERNEL_SIN + """
uniform float eps = 0.00001;
uniform int n;
vec4 f(vec4 x) {
    float x0 = 0.5;
    float summe = x0;
    for (int i = 1; i <= n - 1; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(g(x.x, x0+eps)-g(x.x, x0))/eps);
    }
    return vec4(x.x, summe/n, 0, 1.0);
}
"""

LYAPUNOV_ANALYTISCH = KERNEL_SIN_DIFF + KERNEL_SIN + """
uniform int n = 700;
vec4 f(vec4 x) {
    float x0 = 0.6;
    float summe = log(abs(dg(x.x, x0)));
    for (int i = 1; i <= n; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(dg(x.x, x0)));
    }
    return vec4(x.x, summe/n, 0, 1.0);
}
"""
window = PlotterWindow(axis=(1.0,2.0), origin=(-2.1,2.8),
    bg_color=[1.0,1.0,1.0,1])



log_fnc = lambda r, x: r*sin(x)
imax = 600
rn = 10000
pydomain = domain.PythonCodeDomain(int(rn*float(imax)/2))
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, 300, rn=rn, imax=imax, xs=2.1, xe=3.1, x_0=lambda i: 0.5*(2*(i%2) -1))
pydomain.recalculate_on_prerender = False
pydomain.dimension = 2
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,.2], color_max=[0.0,0.0,0.0,.2])
window.plotter.get_graph('iteration').set_dotsize(0.001)

adomain = domain.Axis(80000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_ANALYTISCH))
window.plotter.get_graph('lyapunov').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
linedomain = domain.Domain(10)
linedomain.push_data([numpy.pi, -8.0, numpy.pi, 0,2*numpy.pi, -8.0, 2*numpy.pi, 0])

window.plotter.add_graph('line', graph.Line2d(linedomain, mode=GL_LINES))
window.plotter.get_graph('line').set_colors(color_min=[1.0,0.0,.0,1], color_max=[1.0,0.0,0.0,1])


lines=  [0.0, 1.570728749999546, 2.4432446071429674, 2.6580499999998904, 2.70599999999986, 2.71600010303040]
for x in lines:
    origin_domain = domain.Domain(2)
    origin_domain.push_data([x, -10.0, x, 10.0])
    window.plotter.add_graph('origin'+str(x), graph.Line2d(origin_domain))
    window.plotter.get_graph('origin'+str(x)).set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

for i in range(0,len(lines)-2):
    print('delta_'+str(i)+'='+str((lines[i+0]-lines[i+1])/(lines[i+1]-lines[i+2])))


uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('eps', 0.01, 0.000001)
uniforms.set_global('n', 700, 2)
window.add_widget('test', widget.Uniforms(uniforms))
window.run()
