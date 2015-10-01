from plotting.app import PlotterWindow
from plotting import graph, domain

KERNEL = """

float fft(float R, float x) {
    
    float sum = 0;
    int fac = 1;
    for(int i=0;i<16;i+=1) {
        fac = max(1, fac*i);
        if (i%2 == 0) {
            sum += 1.0 * 1/fac * 1/fac * pow(x, 2*i) * 1/(2*i+2) * pow(R, 2*i+2);
        }
        else {
            sum -= 1.0 * 1/fac * 1/fac * pow(x, 2*i) * 1/(2*i+2) * pow(R, 2*i+2);
        }
    }

    return sum;


}

uniform float R = 2.0;
vec4 f(vec2 pc) {
    float res;
    float pi = 3.14;
    res =  fft(R, length(pc));
    return vec4(res/(pow(R,2)/2.0), res/(pow(R,2)/2.0), res/(pow(R,2)/2.0), 1);
}
"""

window = PlotterWindow(axis=(5.0,5.0), origin=(2.5, 2.5), plot_time=True)
window.plotter.add_graph('bla', graph.Field2d(KERNEL))

window.run()
