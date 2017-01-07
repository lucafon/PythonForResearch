import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import bernoulli

# G = nx.karate_club_graph()
# nx.draw(G, with_labels = True, node_color='lightblue', edge_color='gray')
# plt.show()

N = 500
p = 0.08

def er_graph(N, p):
	G = nx.Graph()
	G.add_nodes_from(range(N))
	for node1 in G.nodes():
		for node2 in G.nodes():
			if node1 < node2 and bernoulli.rvs(p=p):
				G.add_edge(node1, node2)
	return G

def plot_degree_distribution(G):
	plt.hist(list(G.degree().values()), histtype='step')
	plt.xlabel('Degree $k$')
	plt.ylabel('$P(k)$')
	plt.title('Degree distribution')
	

	
# nx.draw(G, with_labels = True, node_color='lightblue', edge_color='gray')		
# plt.show()	
G1 = er_graph(N, p)
plot_degree_distribution(G1)
G2 = er_graph(N, p)
plot_degree_distribution(G2)
G3 = er_graph(N, p)
plot_degree_distribution(G3)
plt.show()