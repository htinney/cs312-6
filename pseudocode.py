import heapq

class Vertex:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

class Edge:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def length(self):
		pass
	
	def __eq__(self, other):
		return self.p1 == other.p1 and self.p2 == other.p2

class Hull:
	def __init__(self, verts, edges):
		self.verts = verts
		self.edges = edges
	
	def add_edge(self, p1, p2):
		self.edges += Edge(p1, p2)

	def copy(self):
		return Hull(self.verts, self.edges)
	
	# Checks if this edge already exists
	def exists(self, p1, p2):
		pass

	# Checks if edge crosses other edges that already exist
	def crosses(self, p1, p2):
		pass

	# Checks if two points are visible, taking into account the current edges
	def visible(self, p1, p2):
		pass
	
	# Turn the hull into a circuit, deleting unnecessary edges
	# Sets cost to None if a circuit was not found
	def circuitize(self):
		self.cost = None
		pass

	# Compare the most recently added edge as our heuristic
	# If it's smaller, it's more worth visiting
	def __lt__(self, other):
		return self.edges[-1].length < other.edges[-1].length
	
	def __add__(self, other):
		self.verts += other.verts
		self.edges += other.edges

def stitch_hulls(outer_hull, inner_hull):

	# Combine outer hull and inner hull
	outer_hull += inner_hull

	# Expand all options for stitching
	Q = heapq.heapify([])
	outer_hull.circuitize()
	heapq.heappush(Q, outer_hull)

	# Set the minimum hull
	minhull = outer_hull

	while len(Q) > 0:
		hull = heapq.heappop(Q)
		for p1 in hull.verts:
			for p2 in hull.verts:
				if p1 == p2:
					continue
				if hull.exists(p1, p2) or not hull.visible(p1, p2) or hull.crosses(p1, p2):
					continue
				
				newhull = hull.copy()
				newhull.add_edge(p1, p2)
				newhull.circuitize()

				cost = newhull.cost
				if cost is not None and (minhull.cost is None or cost < minhull.cost):
					minhull = newhull
				
				heapq.heappush(Q, newhull)

	return minhull

def convex_hull(verts):
	pass

def tsp_hull_stitching(verts):
	# Create the convex hulls
	hulls = []
	while len(verts) > 0:
		hull = convex_hull(verts)
		hulls.append(hull)
		verts -= hull.verts
	
	final_hull = hull[0]

	for i in range(1, len(hulls)):
		final_hull = stitch_hulls(final_hull, hulls[i])

	return final_hull