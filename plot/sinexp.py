from plotting.app import axis_plot2d
from plotting.util import function_kernel

axis_plot2d(
    function_kernel('sin(20*exp(-x.x*x.x))'),
    function_kernel('exp(-x.x*x.x)')
)
