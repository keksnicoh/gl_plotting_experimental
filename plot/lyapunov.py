#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget

SIMPLE = """
float g(float r, float x) {
    float v = abs(r * cos(x));
    return v;
}

float h(float r, float x) {
    float v = abs(r - 2*r*x);
    return v;
}

float g1(float r, float x) {
    return r*sin(x);
}

float h1(float r, float x) {
    return r*x*(1-x);
}


//vec4 fa(vec4 x) {
//    float y0 = 10;// = g(x.x, x.y);
//    float summe = y0;
//    float n = 10000;
//    for (int i = 1; i < n - 1; i+=1) {
//        y0 = h(x.x, y0);
//        if (i > 300) {
//            summe += log(y0);
//        }
//    }
//    return vec4(x.x, summe/n, 0, 0.3);
//}

uniform float eps;
uniform float n;
vec4 f(vec4 x) {
    //float eps = 0.01;
    float y = 0.8;
    float y0 = y;
    float y1 = y + eps;
    //float n = 10;

    float diff;
    for (int i = 1; i < n; i+=1) {
            //diff = abs(y1-y0);
            //if (diff > eps) {
            //    y1 = y0 + eps;
            //}

            y1 = g1(x.x, y1);
            y0 = g1(x.x, y0);
            
        
    }
    float foo = log(abs((y1 - y0)/eps));

    return vec4(x.x, foo/n, 0, 0.3);
}

"""


window = PlotterWindow(axis=(3.0,7.0), origin=(-1.0,5.0))
#domain = domain.Cartesian(1000, min_y=0.01)
domain = domain.Axis(1000)
#domain.transformation_matrix = domain.fixed_y_transformation
window.plotter.add_graph('lyapunov', graph.Discrete2d(domain, SIMPLE))
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('eps', 0.01)
uniforms.set_global('n', 1.0)
window.add_widget('test', widget.Uniforms(uniforms))
window.run()
