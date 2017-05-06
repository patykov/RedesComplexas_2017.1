from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def findComponents(g, directed):
	comp, hist = graph_tool.topology.label_components(g, directed=directed)
	interest = [54, 57, 134, 143, 230, 242, 243, 251, 259, 260, 261, 278, 280, 281,
				284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296]
	print('{}\n'.format(comp.a))
	for v in interest:
		print('Componente: {} Grau entrada: {} Grau saida: {}\n'.format(comp.a[v], g.vertex(v).in_degree(), g.vertex(v).out_degree()))

if __name__ == '__main__':
	# {Graph path: graph type}
	graphsInfo = {
		# "/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Redes/dolphins/dolphins.gml": ["undirected"],
		# "/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Redes/lesmis/lesmis.gml": ["weighted", "undirected"],
		"/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Redes/celegansneural/celegansneural.gml": ["weighted", "directed"]
	}

	resultPath = "/Users/admin/Documents/UFRJ/RedesComplexas_2017.1/Trabalho2/Results.txt"
	# with open(resultPath, 'w') as file:
	# 	file.write('Trabalho 2 - RedesComplexas_2017\n')

	for graphPath, graphType in graphsInfo.items():
		graphDir = graphPath.replace(graphPath.split('/')[-1], '')
		graphName = graphPath.split('/')[-1]
		g = load_graph(graphPath)

		# Qnt de nos e arestas
		edges = g.get_edges()
		vertices = g.get_vertices()
		count = 0
		for v in vertices:
			if g.vertex(v).in_degree() ==0:
				count+=1
		print count

		weight = None
		if "weighted" in graphType:
			weight = g.edge_properties['value']
		directed = False
		if "directed" in graphType:
			directed = True

		findComponents(g, directed)
		"""
		# Grau total
		grau_total_map = g.degree_property_map("total")
		order_grau = sorted(grau_total_map.a)
		top_grau = order_grau[-10:]
		less_grau = order_grau[:10]
		graph_tool.draw.graph_draw(g, vertex_fill_color=grau_total_map, 
						vertex_size=graph_tool.draw.prop_to_size(grau_total_map, mi=5, ma=20), 
						vcmap=plt.cm.gist_heat, vorder=grau_total_map, vertex_text=g.vertex_index, 
						output=graphDir+'draw_grau_total.png')
		# if directed:
		# 	grau_in_map = g.degree_property_map("in")
		# 	grau_out_map = g.degree_property_map("out")
		# 	top_grau_in = sorted(grau_in_map.a, reverse=True)[:10]
		# 	top_grau_out = sorted(grau_out_map, reverse=True)[:10]
		# 	graph_tool.draw.graph_draw(g, vertex_fill_color=grau_in_map, 
		# 				vertex_size=graph_tool.draw.prop_to_size(grau_in_map, mi=5, ma=20), 
		# 				vcmap=plt.cm.gist_heat, vorder=grau_in_map, vertex_text=g.vertex_index, 
		# 				output=graphDir+'draw_grau_in.png')
		# 	graph_tool.draw.graph_draw(g, vertex_fill_color=grau_out_map, 
		# 				vertex_size=graph_tool.draw.prop_to_size(grau_out_map, mi=5, ma=20), 
		# 				vcmap=plt.cm.gist_heat, vorder=grau_out_map, vertex_text=g.vertex_index, 
		# 				output=graphDir+'draw_grau_out.png')
		
		# Betwenness
		vb_map, eb_map = graph_tool.centrality.betweenness(g, weight=weight)
		order_betwenness = sorted(vb_map.a)
		top_betwenness = order_betwenness[-10:]
		less_betwenness = order_betwenness[:10]
		graph_tool.draw.graph_draw(g, vertex_fill_color=vb_map, 
						vertex_size=graph_tool.draw.prop_to_size(vb_map, mi=5, ma=20), 
						vcmap=plt.cm.gist_heat, vorder=vb_map, vertex_text=g.vertex_index, 
						output=graphDir+'draw_betwenness.png')

		# Katz
		katz_map = graph_tool.centrality.katz(g, weight=weight)
		order_katz = sorted(katz_map.a)
		top_katz = order_katz[-10:]
		less_katz = order_katz[:10]
		graph_tool.draw.graph_draw(g, vertex_fill_color=katz_map, 
						vertex_size=graph_tool.draw.prop_to_size(katz_map, mi=5, ma=20), 
						vcmap=plt.cm.gist_heat, vorder=katz_map, vertex_text=g.vertex_index, 
						output=graphDir+'draw_katz.png')

		# Pagerank
		pagerank_map = graph_tool.centrality.pagerank(g, weight=weight)
		order_pagerank = sorted(pagerank_map.a)
		top_pagerank = order_pagerank[-10:]
		less_pagerank = order_pagerank[:10]
		graph_tool.draw.graph_draw(g, vertex_fill_color=pagerank_map, 
						vertex_size=graph_tool.draw.prop_to_size(pagerank_map, mi=5, ma=20), 
						vcmap=plt.cm.gist_heat, vorder=pagerank_map, vertex_text=g.vertex_index, 
						output=graphDir+'draw_pagerank.png')

		# Closeness
		g1 = graph_tool.GraphView(g, vfilt=graph_tool.topology.label_largest_component(g, directed=directed))
		closeness = graph_tool.centrality.closeness(g1, weight=weight)
		order_closenness = sorted(closeness)
		top_closenness = order_closenness[-10:]
		less_closenness = order_closenness[:10]
		graph_tool.draw.graph_draw(g1, vertex_fill_color=closeness, 
						vertex_size=graph_tool.draw.prop_to_size(closeness, mi=5, ma=20), 
						vcmap=plt.cm.gist_heat, vorder=closeness, vertex_text=g.vertex_index, 
						output=graphDir+'draw_closeness.png')


		# Write results to a file
		with open(resultPath, 'a') as file:
			file.write('{:<15}: {}\n'.format('Graph', graphName))
			file.write('{:<15}: {:^8}, {:<8}: {:^8}\n'.format('Arestas', len(edges), 'Vertices', len(vertices)))
			
			# Grau total
			file.write('Maior\n')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Grau Total'))
			for i, grau in enumerate(top_grau):
				v = [vi for vi in vertices if grau_total_map[vi]==grau]
				file.write('{:<3}. {:10} ({:5})\n'.format(i+1, v, grau))
			file.write('Menor\n')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Grau Total'))
			for i, grau in enumerate(less_grau):
				v = [vi for vi in vertices if grau_total_map[vi]==grau]
				if len(v)>= 10:
					file.write('{} vertices with grau total = {}\n'.format(len(v), grau))
					file.write('{:10} ({:5})\n'.format(v, grau))
					break
				file.write('{:<3}. {:10} ({:5})\n'.format(i+1, v, grau))
		
			# if directed:
			# 	# Grau de entrada
			# 	file.write('\n{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Grau Entrada'))
			# 	for i, grau in enumerate(top_grau_in):
			# 		v = [vi for vi in vertices if grau_in_map[vi]==grau]
			# 		file.write('{:<3}. {:10} ({:5})\n'.format(i+1, v, grau))
			# 	# Grau de saida
			# 	file.write('\n{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Grau Saida'))
			# 	for i, grau in enumerate(top_grau_out):
			# 		v = [vi for vi in vertices if grau_out_map[vi]==grau]
			# 		file.write('{:<3}. {:10} ({:5})\n'.format(i+1, v, grau))
			
			# Betwenness
			file.write('Maior\n')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Betwenness'))
			for i, b in enumerate(top_betwenness):
				v = [vi for vi in vertices if vb_map[vi]==b]
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, b))
			file.write('Menor\n')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Betwenness'))
			for i, b in enumerate(less_betwenness):
				v = [vi for vi in vertices if vb_map[vi]==b]
				if len(v)>=10:
					file.write('{} vertices with betweenness = {}\n'.format(len(v), b))
					file.write('{:10} ({:5})\n'.format(v, b))
					break
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, b))
			
			# Katz
			file.write('\nMaior')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Katz'))
			for i, k in enumerate(top_katz):
				v = [vi for vi in vertices if katz_map[vi]==k]
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, k))
			file.write('\nMenor')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Katz'))
			for i, k in enumerate(less_katz):
				v = [vi for vi in vertices if katz_map[vi]==k]
				if len(v)>=10:
					file.write('{} vertices with katz = {}\n'.format(len(v), k))
					file.write('{:10} ({:5})\n'.format(v, k))
					break
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, k))
			
			# PageRank
			file.write('Maior\n')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'PageRank'))
			for i, p in enumerate(top_pagerank):
				v = [vi for vi in vertices if pagerank_map[vi]==p]
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, p))
			file.write('\nMenor')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'PageRank'))
			for i, p in enumerate(less_pagerank):
				v = [vi for vi in vertices if pagerank_map[vi]==p]
				if len(v)>=10:
					file.write('{} vertices with pagerank = {}\n'.format(len(v), p))
					file.write('{:10} ({:5})\n'.format(v, p))
					break
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, p))
			
			# Closenness
			file.write('\nMaior')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Closenness'))
			for i, c in enumerate(top_closenness):
				v = [vi for vi in vertices if closeness.a[vi]==c]
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, c))
			file.write('\nMenor')
			file.write('{:<3}. {:10} ({:5})\n'.format('', 'Vertice', 'Closenness'))
			for i, c in enumerate(less_closenness):
				v = [vi for vi in vertices if closeness.a[vi]==c]
				if len(v)>=10:
					file.write('{} vertices with closenness = {}\n'.format(len(v), c))
					file.write('{:10} ({:5})\n'.format(v, c))
					break
				file.write('{:<3}. {:10} ({:5.3})\n'.format(i+1, v, c))
			file.write('-----------------\n\n')



 """





