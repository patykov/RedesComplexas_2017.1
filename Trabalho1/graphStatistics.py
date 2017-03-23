from graph_tool.all import *
import numpy as np
import sys
import os

if __name__ == '__main__':
	graphPath = sys.argv[1]
	if graphPath.endswith('.gml'):
		g = load_graph(graphPath)
	else:
		raise Exception('Please provide an .gml graph format')

	edges = g.get_edges()
	g = GraphView(g, vfilt=label_largest_component(g))
	vb, eb = graph_tool.centrality.betweenness(g)
	graph_draw(g, pos=g.vb["pos"], vertex_fill_color=vb, vertex_size=graph_tool.prop_to_size(vb, mi=5, ma=15),
		            edge_pen_width=graph_tool.prop_to_size(eb, mi=0.5, ma=5), vcmap=matplotlib.cm.gist_heat,
		            vorder=vb, output="betweenness.pdf")
