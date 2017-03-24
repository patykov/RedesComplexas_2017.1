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

	# vb, eb = betweenness(g)
	# graph_draw(g, pos=g.vb["pos"], vertex_fill_color=vb, vertex_size=graph_tool.prop_to_size(vb, mi=5, ma=15),
	# 	            edge_pen_width=graph_tool.prop_to_size(eb, mi=0.5, ma=5), vcmap=matplotlib.cm.gist_heat,
	# 	            vorder=vb, output="betweenness.pdf")

	# hist = graph_tool.stats.distance_histogram(g, samples=20)
	# print(hist)

	# Grau Medio
	grau_medio, dp_grau_medio = graph_tool.stats.vertex_average(g, 'total')
	print(grau_medio, dp_grau_medio)

	# Menor distancia
	dist_map = graph_tool.topology.shortest_distance(g)
	dist, dp_dist = graph_tool.stats.vertex_average(g, dist_map)
	shortest_dist = np.amin(dist)
	dp_shortest_dist = [dp_dist[i] for (i,x) in enumerate(dist) if x==shortest_dist]
	print(shortest_dist, dp_shortest_dist)

