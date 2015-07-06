OpenGL plotting experiments
============================
Nicolas Heimann

Jeese Hinrichsen

 
bifurcation diagramm with translated (+0,6384) lyapunov exponent
![bifurkation von r*sin mit cos fit](/results/bifurc-logistic-translated-lyapunov.jpg)


problems with the iterations: before fixing
![bifurkation von r*sin mit cos fit](/results/bad-iteration.png)


currently its possible to plot a 1d/2d domain on a x-y cartesian space. here is a image from a
bifurcation animation of the logistic function. the plotter shows from iter_max=0 to iter_max=100
an animation of the bifurcation diagramm. in this image 16.000.000 (x,r) values where rendered.

![bifurkation von r*sin mit cos fit](/bifurk2.png)

animated plot of 50 2d wave function aligned on a line axis in vertex shader (320000 buffer entries)

![bifurkation von r*sin mit cos fit](/waveplot.png)


old and experiments
-------------------

plotting experiment: numpy arrays with length 2000200 + 100000
![bifurkation von r*sin mit cos fit](/plot_bifurcation_sin_with_cos_fit.jpg)



framebuffer implementation for managing multiple plots or
implement frames for the plot it self to increase performance.
this is a screenshot from demos.layout demo script
![bifurkation von r*sin mit cos fit](/layout_demo.png)
