from plotting.app import PlotterWindow
from plotting import graph, domain



window = PlotterWindow()
domain = domain.Cartesian(100, min_y=0.3)
window.plotter.add_graph('bifurkation', graph.Discrete2d(domain))
window.run()
