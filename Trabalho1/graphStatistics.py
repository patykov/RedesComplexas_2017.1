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

	# Grau Medio
	grau_medio, dp_grau_medio = graph_tool.stats.vertex_average(g, 'total')
	print(grau_medio, dp_grau_medio)

	# Menor distancia
	dist_map = graph_tool.topology.shortest_distance(g)
	dist, dp_dist = graph_tool.stats.vertex_average(g, dist_map)
	shortest_dist = np.amin(dist)
	dp_shortest_dist = [dp_dist[i] for (i,x) in enumerate(dist) if x==shortest_dist][0]
	print(shortest_dist, dp_shortest_dist)

	# Betwenness
	vb_map, eb_map = graph_tool.centrality.betweenness(g)
	vb, dp_vb = graph_tool.stats.vertex_average(g, vb_map)
	print(vb, dp_vb)
