#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
from numpy import log

flog = lambda r,x : r*x*(1-x)
dflog = lambda r,x : r-2*r*x

r = 3.0
x0 = 0.5
summe = log(abs(dflog(r, x0)))
print(summe)


for i in range(0, 1000):
    x0 = flog(r, x0)
    print('x0', x0)
    summe += log(abs(dflog(r, x0)))
    print(summe)
print(summe/1000)


GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, 6*x.y-4.0, x.z, 1.0);
}
"""
KERNEL_LOG = "float g(float r, float x) {return r * x * (1-x);}\n"
KERNEL_LOG_DIFF = "float dg(float r, float x) {return r-2.0*r*x;}\n"
LYAPUNOV_NORMIERT = KERNEL_LOG + """
uniform float eps = 0.00001;
uniform int n_check = 5;
uniform int n;
vec4 f(vec4 x) {
    float x0 = x.y;
    float summe = x0;
    float summe500 = 0.0f;
    for (int i = 1; i <= n - 1; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(g(x.x, x0+eps)-g(x.x, x0))/eps);
        if (i == n_check) {
            summe500 = summe;
        }
    }
    summe = summe/n;
    summe500 = summe500/n_check;
    float res = exp(-500*pow(summe-summe500,2));

    return vec4(x.x, x.y, 1.0-res, 1.0);
}
"""

LYAPUNOV_ANALYTISCH = KERNEL_LOG_DIFF + KERNEL_LOG + """
uniform int n;
uniform int n_check = 5;
vec4 f(vec4 x) {
    float x0 = x.y;

    float summe = log(abs(dg(x.x, x0)));
    float summe500 = 0.0f;
    for (int i = 1; i <= n; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(dg(x.x, x0)));

        if (i == n_check) {
            summe500 = summe;
        }

    }
    summe = summe/n;
    summe500 = summe500/n_check;
    float res = exp(-500*pow(summe-summe500,2));

    return vec4(x.x, x.y, 1.0-res, 1.0);
}
"""


window = PlotterWindow(axis=(4.0,1.0), origin=(-0.0,0.0), bg_color=[1,1,1,1], x_label='r', y_label='Bifurkation Logistische Abblidung')

adomain = domain.Cartesian(700)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_NORMIERT))
window.plotter.get_graph('lyapunov').set_colors(color_min=[.0,.0,.0,1.0], color_max=[1.0,1.0,1.0,1.0])
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('n', 10000)

window.run()
