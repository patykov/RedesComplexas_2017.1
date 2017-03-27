from graph_tool.all import *
import numpy as np
from pylab import *
import sys
import os

if __name__ == '__main__':
	# Graph path: graph type
	graphsInfo = {
		"/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Trabalho1/dolphins/dolphins.gml": ["undirected"],
		"/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Trabalho1/lesmis/lesmis.gml": ["weighted", "undirected"],
		"/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Trabalho1/celegansneural/celegansneural.gml": ["weighted", "directed"]
	}

	for graphPath, graphType in graphsInfo.items():
		print('\n{:<21}: {}'.format('Graph', graphPath.split('/')[-1]))

		#Check graph format
		if graphPath.endswith('.gml'):
			g = load_graph(graphPath)
		else:
			raise Exception('Please provide an .gml, .gt, .xml or .dot graph format')
		graphDir = graphPath.replace(graphPath.split('/')[-1], '')

		# pos = graph_tool.draw.sfdp_layout(g)
		# graph_tool.draw.graph_draw(g, pos=pos, vertex_text=g.vertex_index, output=graphDir+"graph-draw-sfdp.pdf")
		# pos = graph_tool.draw.arf_layout(g, max_iter=0)
		# graph_tool.draw.graph_draw(g, pos=pos, vertex_text=g.vertex_index, output=graphDir+"graph-draw-arf.pdf")

		# Qnt de nos e arestas
		edges = g.get_edges()
		vertices = g.get_vertices()

		weight = None
		if "weighted" in graphType:
			weight = g.edge_properties['value']
		print ('{:<21}: {:^10}, {:<15}: {:^10}'.format('Arestas', len(edges), 'Vertices', len(vertices)))

		# Grau Medio
		grau_medio, dp_grau_medio = graph_tool.stats.vertex_average(g, 'total')
		print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Grau medio total', grau_medio, 'desvio padrao', dp_grau_medio))
		directed = False
		if "directed" in graphType:
			directed = True
			grau_medio_in, dp_grau_medio_in = graph_tool.stats.vertex_average(g, 'in')
			grau_medio_out, dp_grau_medio_out = graph_tool.stats.vertex_average(g, 'out')
			print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Grau medio de entrada', grau_medio_in, 'desvio padrao', dp_grau_medio_in))
			print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Grau medio de saida', grau_medio_out, 'desvio padrao', dp_grau_medio_out))


		# Grau hist
		grau_hist = graph_tool.stats.vertex_hist(g, 'total')
		y = [float(x/sum(grau_hist[0])) for x in grau_hist[0]]

		figure(figsize=(10,6))
		gca().plot(grau_hist[1][:-1], y, 'bo', alpha=0.7, linestyle='None')
		subplots_adjust(left=0.2, bottom=0.2)
		xlabel("$Grau_{k}$")
		ylabel("PDF P[D=k]")
		tight_layout()
		savefig(graphDir+"deg-dist.pdf")

		# Menor distancia
		# short_dist_map = graph_tool.topology.shortest_distance(g, weights=weight) # A menor distancia entre todos os pares de vertices
		# mean_short_dist, dp_short_dist = graph_tool.stats.vertex_average(g, short_dist_map) # A menor distancia media para cada vertice com seu dp
		# shortest_mean_dist = np.amin(mean_short_dist) # O vertice com a menor distancia media
		# dp_shortest_mean_dist = [dp_short_dist[i] for (i,x) in enumerate(mean_short_dist) if x==shortest_mean_dist][0]
		# print('{:<15}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Menor dist media', shortest_mean_dist, 'desvio padrao', dp_shortest_mean_dist))

		# Betwenness
		vb_map, eb_map = graph_tool.centrality.betweenness(g, weight=weight)
		vb_media, dp_vb = graph_tool.stats.vertex_average(g, vb_map)
		print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Betwenness media', vb_media, 'desvio padrao', dp_vb))

		# Katz
		katz_map = graph_tool.centrality.katz(g, weight=weight)
		katz_media, dp_katz = graph_tool.stats.vertex_average(g, katz_map)
		print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Katz media', katz_media, 'desvio padrao', dp_katz))

		# Pagerank
		pagerank_map = graph_tool.centrality.pagerank(g, weight=weight)
		pagerank_media, dp_pagerank = graph_tool.stats.vertex_average(g, pagerank_map)
		print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Pagerank media', pagerank_media, 'desvio padrao', dp_pagerank))

		# Componentes
		comp, hist = graph_tool.topology.label_components(g, directed=directed)
		number_of_components = len(np.unique(comp.a))
		bigger_component = np.unique(np.where(hist==max(hist)))
		print('{:<21} {:^11}, {:<15}: {:^10}'.format('Conected componentes:', number_of_components, 'bigger', int(bigger_component)))
		if number_of_components > 1:
			x = comp.a
			figure(figsize=(10,6))
			gca().hist(x, max(x), facecolor='green', alpha=0.7)
			subplots_adjust(left=0.2, bottom=0.2)
			xlabel("Component id")
			ylabel("Number of vertices")
			tight_layout()
			savefig(graphDir+"conected-components.pdf")

	# Clusterizacao local
	clust = graph_tool.clustering.local_clustering(g)
	clust_media, dp_clust = graph_tool.stats.vertex_average(g, clust)
	print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Local Clust. media', clust_media, 'desvio padrao', dp_clust))

	# Clusterizacao global
	global_clust, dp_global_clust = graph_tool.clustering.global_clustering(g)
	print('{:<21}: {:^10.5f}, {:<15}: {:^10.5f}'.format('Global Clust.', global_clust, 'desvio padrao', dp_global_clust))

