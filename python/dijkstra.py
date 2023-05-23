import heapq
import osmnx as ox

# Default region(only consider routes in this region/place)
DEFAULT_REGION = "Amherst, MA"

# Term to find in both stop and start locations. If input does not include these, return error.
SEARCH_TERM = "amherst"
# All possible route types for the application
POSSIBLE_ROUTE_TYPES = ["drive", "walk", "bike"]
# All possibl elevation gain types
POSSIBLE_ELEVATION_GAIN_TYPES = ["minimize", "maximize"]

def get_shortest_length_path(G, start, end):
	queue = []
	heapq.heappush(queue, (0, start))
	prevNodes = {}
	prevNodes[start] = 0
	costs = {}
	costs[start] = 0

	while len(queue) > 0:
		_ , curNode = heapq.heappop(queue)
		if curNode == end:
			break
		for curNode, nextNode in G.edges(curNode):
			edgeLength = G.edges[curNode, nextNode, 0]['length']
			if nextNode not in costs or costs[nextNode] > (costs[curNode] + edgeLength):
				costs[nextNode] = costs[curNode] + edgeLength
				heapq.heappush(queue, (costs[nextNode], nextNode))
				prevNodes[nextNode] = curNode
	return generate_path(prevNodes, start, end)

def generate_path(prevNodes, start, end):
	path = []
	curNode = end
	path.append(curNode)
	while curNode != start:
		curNode = prevNodes[curNode]
		path.append(curNode)
	return path[::-1]

def calculate_path_length(G, path):
	total_length = 0
	for i in range(len(path) - 1):
		total_length += G.edges[path[i], path[i+1], 0]['length']
	return total_length

def algorithm(start_location:str, stop_location:str, route_type:str, elevation_gain_type:str, max_dist:int, API_KEY:str, to_geocode:bool):
   # Input checks
    vars = [start_location, stop_location, route_type, elevation_gain_type, max_dist, API_KEY]
    for var in vars:
        if var is None or (type(var) != str and type(var) != int):
            return None

    if type(to_geocode) != bool:
        return None

    if route_type.lower() not in POSSIBLE_ROUTE_TYPES:
        return None

    if elevation_gain_type.lower() not in POSSIBLE_ELEVATION_GAIN_TYPES:
        return None

    if float(max_dist) < 0 or float(max_dist) > 100:
        return None

    if "amherst" not in start_location.lower():
        return []

    if "amherst" not in stop_location.lower():
        return []

    multiplier = 1 if elevation_gain_type == "minimize" else -1

    # Geocoding the start and stop locations to get their latitude and longitudes.
    geocode_start = ox.geocode(start_location)
    geocode_start_lat = geocode_start[0]
    geocode_start_lon = geocode_start[1]

    geocode_stop = ox.geocode(stop_location)
    geocode_stop_lat = geocode_stop[0]
    geocode_stop_lon = geocode_stop[1]

    G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
    G = ox.elevation.add_node_elevations_google(G, API_KEY)


    # Finding the nearest nodes to the start and stop exact geocodes in the final graph
    start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
    destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

    shortest_path_by_distance = get_shortest_length_path(G, start, destination)
    shortestDistance = calculate_path_length(G, shortest_path_by_distance)

    upper_limit_distance_percentage = (100 + float(max_dist))
    lower_limit_distance_percentage = 100

    #Boolean value to exit while loop once the shortest path within the maximum distance is found
    path_found = False

    while lower_limit_distance_percentage <= upper_limit_distance_percentage and path_found == False:
        acceptablePathLength = (lower_limit_distance_percentage/100)*shortestDistance
        queue = []
        heapq.heappush(queue, (0, start))
        prevNodes = {}
        costs = {}
        costs[start] = 0
        elevation_gain_per_node = {}
        prevNodes[start] = 0
        elevation_gain_per_node[start] = 0
        while len(queue) > 0:
            _ , curNode = heapq.heappop(queue)
            if curNode == destination:
                if costs[curNode] <= acceptablePathLength:
                    path = generate_path(prevNodes ,start, destination)
                    path_found = True
                    break
            for curNode, nextNode in G.edges(curNode):  
                edgeLength = G.edges[curNode, nextNode, 0]['length']
                elevationGain = G.nodes[nextNode]['elevation'] - G.nodes[curNode]['elevation']
                # elevationGain = elevations[nextNode] - elevations[curNode]
                if nextNode not in costs or costs[nextNode] > (costs[curNode] + edgeLength):
                    if elevationGain > 0:
                        elevation_gain_per_node[nextNode] = elevation_gain_per_node[curNode] + elevationGain
                    else:
                        elevation_gain_per_node[nextNode] = elevation_gain_per_node[curNode]
                    costs[nextNode] = costs[curNode] + edgeLength
                    heapq.heappush(queue, (((multiplier)*elevation_gain_per_node[nextNode]), nextNode))
                    prevNodes[nextNode] = curNode
        lower_limit_distance_percentage += 0.5
    if to_geocode:
        if path_found:
            formatted_path = []
            for node in path:
                formatted_path.append([G.nodes[node]['x'], G.nodes[node]['y']] )
            return formatted_path
        else:
            return []
    else:
         return path