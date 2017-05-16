import random
def min_cut(graph):
	edge_graph = make_edge_graph(graph)
	vertex_graph = copy.deepcopy(graph)
	vertex_graph['A'] = {}
	vertex_graph['B'] = {}
	while len(vertex_graph) > 2:
		vi, vj = edge_graph.pop(random.randrange(len(edge_graph)))
		nb = vertex_graph[vi].keys() + vertex_graph[vj].keys()
		nb = filter(lambda x: x not in (vi, vj), nb)
		del vertex_graph[vi]
		del vertex_graph[vj]
		super_node = 'B' if 'B' in nb else 'A'
		for nb in vertex_graph[vi]:
			pass
		# else


	return len(g), a, b

class EdgeGraph(object):
	"""docstring for EdgeGraph"""
	def __init__(self, adjacencies):
		super(EdgeGraph, self).__init__()

		# these explored discovery tactics are 1 dimensional from v0 to v1
		def not_explored(v0, v1, explored):
			return not(v0 in explored and v1 in explored[v0])

		def mark_explored(v0, v1, explored):
			explored[v1] = explored.get(v1, {})
			explored[v1][v0] = True

		explored = {}
		edges = {} # to keep track of all edges
		vertex_edges = {} # to keep track of which edges are associated with which vertex

		for v0, vs in adjacencies.iteritems():
			vertex_edges[v0] = vertex_edges.get(v0, {})

			# arrange connections in buckets
			ds = {}
			for vi in vs:
				ds[vi] = ds.get(vi, 0) + 1

			for vi, counts in ds.iteritems():
				if not_explored(v0, vi, explored):
					new_edges = [(v0, vi, iden) for iden in range(counts)]
					new_edges_dict = {e: True for e in new_edges}

					# VED
					vertex_edges[vi] = vertex_edges.get(vi, {})
					for v in (v0, vi):
						vertex_edges[v].update(new_edges_dict)

					# ED
					edges.update(new_edges_dict)

					mark_explored(v0, vi, explored)

		self.edges = edges
		self.vertex_edges = vertex_edges

	def pick_random_edge(self):
		return random.choice(self.edges.keys())

	def remove_edge(self, edge):
		def remove(edge, edge_dict):
			def rm(v0, v1, ed):
				'''remove all identified edges (v0, v1, [0 1 2 ...])'''
				iden = 0
				while (v0, v1, iden) in ed:
					del ed[(v0, v1, iden)]
					iden += 1

			v0, v1 = edge
			rm(v0, v1, edge_dict)
			rm(v1, v0, edge_dict)

		#	ED
		remove(edge, self.edges)

		# 	VED
		remove(edge, self.vertex_edges[edge[0]])
		remove(edge, self.vertex_edges[edge[1]])

	def map_changes_from_contraction(self, edge):
		# change name
		# change all edges that contain either v0 and v1 to the new contracted node
		def get_name_map(old, new, iden_edges):
			"""Change any old node into new name"""
			is_affected = lambda e: old in e[:2]
			affected_edges = filter(is_affected, iden_edges)
			def change(old, new, e):
				v0 = [e[0], new][e[0] == old]
				v1 = [e[1], new][e[1] == old]
				return type(e)((v0, v1) + e[2:])

			name_map = {k:change(old, new, k) for k in affected_edges}
			return name_map

		def adjust_identities(name_map, check_lists):
			""" Change identities of contracted vertices to avoid collisons """
			def collided(item, lists):
				return any([item in li for li in lists])

			nm = copy.deepcopy(name_map)
			for old_edge, new_edge in nm.iteritems():
				while collided(new_edge, check_lists + [nm.values()]):
					iden = new_edge[-1] + 1
					new_edge = new_edge[:2] + (iden,)
				nm[old_edge] = new_edge
			return nm

		v0, v1 = edge[:2]
		# new_vertex = '{},{}'.format(v0, v1) # the comma is super important, without commas collisons prevail
		new_vertex = v0

		name_map = {}
		new_edges = {}
		shorcut_edges = (edge[:2], edge[:2][::-1])
		contracted_edges = set()
		for old_vertex in (v0, v1):
			nm = get_name_map(old_vertex, new_vertex, self.vertex_edges[old_vertex].keys())
			# remove contracted edges - edge which comprised of v0 and v1
			nm = adjust_identities(nm, [self.edges, name_map.values()])
			contracted_edges = contracted_edges.union(filter(lambda e: e[:2] in shorcut_edges, nm.keys()))
			nm = {old:new for old, new in nm.iteritems() if old[:2] not in shorcut_edges}
			# if edge == ('32', '5'): print 'nm', nm
			name_map.update(nm)

			# new node gets all connection of old nodes
			# new_edges.update({v: True for v in nm.values()})

		new_edges = {v:True for v in name_map.values()}
		return {new_vertex:new_edges}, name_map, contracted_edges

	def contract(self, edge):
		# print 'Contracting edge', edge
		# print self.edges.keys()
		# print self.vertex_edges

		# remove edges contain both v0 and v1
		self.remove_edge(edge)

		new_element, name_map, contracted_edges = self.map_changes_from_contraction(edge)
		# nm = adjust_identities(name_map, self.edges)
		# print 'old name_map', name_map
		# print 'new name_map', nm
		# name_map = nm

		# if edge == ('14', '2'): print 'name_map', name_map

		affected_vertices = set([v for e in name_map for v in e[:2]]).difference(edge[:2])

		for v in affected_vertices:
			try:
				ve = self.vertex_edges[v]
			except KeyError:
				print 'while contracting edge [{}]'.format(edge)
				print 'vertex [{}] not in ve {}'.format(v, self.vertex_edges.keys())
				print 'name_map', name_map
				print 'affected_vertices', affected_vertices
				raise
			self.vertex_edges[v] = {name_map.get(k, k): True for k in ve}

		# Sanitizing
		# this is the whole point of using vertex_edges, to track affected changes to edges and change it
		# accordingly in the main self.edges
		for old, new in name_map.iteritems():
			# if edge == ('14', '2'): print 'deleting', old
			# if edge == ('14', '2'): print 'adding', new
			# if edge == ('14', '2'): print 'Edges', self.edges.keys()
			# try:
			# 	del self.edges[old]
			# except KeyError:
			# 	print '{} not in {}'.format(old, self.edges.keys())
			# 	raise
			del self.edges[old]
			self.edges[new] = True
			# if edge == ('14', '2'): print 'Edges', self.edges.keys()

		# print 'contracted', contracted_edges
		for edge in contracted_edges:
			del self.edges[edge]

		del self.vertex_edges[edge[0]]
		del self.vertex_edges[edge[1]]
		self.vertex_edges.update(new_element)

	def size(self):
		return len(self.edges)
		

def _min_cut(edge_graph):
	# edge_graph = make_edge_graph(graph)
	while True:
		# choose random
		# vi, vj = edge_graph.pop(random.randrange(len(edge_graph)))
		vi, vj = edge_graph[random.randrange(len(edge_graph))]
		new_edge_graph = filter(lambda e: e not in [[vi, vj], [vj, vi]], edge_graph)
		stat = 'picking [{}] and [{}], edges {}'.format(vi, vj, len(edge_graph))
		# print edge_graph
		if len(new_edge_graph) < 2:
			# print len(edge_graph), edge_graph
			# print 'stopped when', stat
			return len(edge_graph), edge_graph[0]
		else:
			pass
			# print stat

		edge_graph = new_edge_graph

		# make name
		# new_node = ','.join([vi, vj])
		new_node = vi

		# filter either vertices of the edge
		edge_graph = [[new_node if v in (vi, vj) else v for v in edge] for edge in edge_graph]
		# remove self-loop
		# edge_graph = filter(lambda e: e != [new_node, new_node], edge_graph)

import copy
def min_cut(edge_graph):
	m = len(edge_graph)

	mc = (m, None)
	for i in range(m):
		g = copy.deepcopy(edge_graph)
		new_cut = _min_cut(g)
		mc = min(mc, new_cut)
		print 'Attemp No. {}:'.format(i), mc, new_cut
	return mc

def min_cut2(adjacencies):
	def _min_cut2(graph):
		while True:
			# print map(lambda e: e[:], graph.edges.keys())
			# choose random]
			size = graph.size()
			edges = None # graph.edges.keys()

			edge = graph.pick_random_edge()[:2]
			graph.contract(edge)

			if graph.size() < 2:
				return size, edges

	mc = (10e6, None)
	n = len(adjacencies)
	for i in range(n**2):
		eg = EdgeGraph(copy.deepcopy(adjacencies))
		new_cut = _min_cut2(eg)
		mc = min(mc, new_cut)
		print 'Attemp No. {}:'.format(i), mc, new_cut
	return mc


def read_adjacencies(f):
	data = open(f, 'r').read()
	data = filter(bool, data.split('\n'))
	# data = [map(int, a.split()) for a in data]
	data = [a.split() for a in data]
	return data

def make_edge_graph(data):
	graph = []
	explored = {}
	for adj in data:
		v0 = adj[0]
		nodes = adj[1:]
		# graph += [(adj[0], adj_i) for adj_i in nodes]
		for vi in nodes:
			if not(v0 in explored and vi in explored[v0]):
				graph.append((v0, vi))
				explored[vi] = explored.get(vi, {})
				explored[vi][v0] = True
	return graph

def make_adjacency_graph(data):
	return {adj[0]: adj[1:] for adj in data}

def make_vertex_graph(data):
	for adj in data:
		v0 = adj[0]
		nodes = adj[1:]
		graph[v0] = graph.get(v0, {})
		for vi in nodes:
			graph[vi] = graph.get(vi, {})
			graph[v0][vi] = 1
			graph[vi][v0] = 1

	return graph

def test():
	graph = {
		1: [3, 2, 3],
		2: [1, 3],
		3: [1, 2, 1]
	}

	eg = EdgeGraph(copy.deepcopy(graph))
	assert eg.edges == {(1, 2, 0): True, (1, 3, 0): True, (1, 3, 1): True, (2, 3, 0): True}
	assert eg.vertex_edges == {1: {(1, 2, 0): True, (1, 3, 0): True, (1, 3, 1): True}, 2: {(1, 2, 0): True, (2, 3, 0): True}, 3: {(1, 3, 0): True, (1, 3, 1): True, (2, 3, 0): True}}

	eg.contract((1,3))
	assert eg.edges == {(2, 1, 0): True, (1, 2, 0): True}
	assert eg.vertex_edges == {2: {(2, 1, 0): True, (1, 2, 0): True}, 1: {(2, 1, 0): True, (1, 2, 0): True}}

	min_cut2(graph)


	edge_graph = [
		('1', '2'),
		('1', '3'),
		('2', '3'),
		('2', '4'),
		('3', '4'),
	]
	print 'Min cut for {} is {}'.format(edge_graph, min_cut(edge_graph))


def test_big():
	input_file = 'tests/course1/assignment4MinCut/input_random_15_50.txt'
	output_file = input_file.replace('input', 'output')
	adjacencies = read_adjacencies(input_file)

	graph = make_adjacency_graph(adjacencies)

	# eg = EdgeGraph(graph)
	# # print eg.edges
	# eg.contract(('3','2'))
	# print 'eg.edges', eg.edges.keys()
	# print 'eg.vertex_edges', {k:v.keys() for k,v in eg.vertex_edges.iteritems()}

	# print '\n'

	# eg.contract(('32','5'))
	# print 'eg.edges', eg.edges.keys()
	# print 'eg.vertex_edges', {k:v.keys() for k,v in eg.vertex_edges.iteritems()}
	# eg.contract(('325','4'))
	# print 'eg.edges', eg.edges.keys()
	# print 'eg.vertex_edges', {k:v.keys() for k,v in eg.vertex_edges.iteritems()}
	# eg.contract(('325','4'))

	cuts, _ = min_cut2(graph)


	edge_graph = make_edge_graph(adjacencies)
	cuts, _ = min_cut(edge_graph)
	expected_cuts = int(open(output_file, 'r').read())
	assert cuts == expected_cuts, 'RCut {}, expected {}'.format(cuts, expected_cuts)

def test_assignment():
	input_file = 'kargerMinCut.txt'
	adjacencies = read_adjacencies(input_file)
	edge_graph = make_edge_graph(adjacencies)
	min_cut(edge_graph)

# test()
test_big()
# test_assignment()