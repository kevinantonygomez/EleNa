import osmnx as ox
import networkx as nx
from queue import PriorityQueue
from typing import Callable

# Default region(only consider routes in this region/place)
DEFAULT_REGION = "Amherst, MA"
# The network type. We don't want bounding box we want network type distance between nodes, not absolute euclidian distance.
DIST_TYPE = "network"
# Length attribute name for length of edges in graph
LENGTH_ATTR = "length"
# Elevation attribute name for elevation of nodes in graph
ELEVATION_ATTR = "elevation"
# Term to find in both stop and start locations. If input does not include these, return error.
SEARCH_TERM = "amherst"
# All possible route types for the application
POSSIBLE_ROUTE_TYPES = ["drive", "walk", "bike"]
# All possibl elevation gain types
POSSIBLE_ELEVATION_GAIN_TYPES = ["minimize", "maximize"]

def calculate_elevation_gain(graph:nx.MultiDiGraph, nodes:list) -> int:
    ind = 0
    gain = 0
    # Iterate through pairs of adjacent nodes and calculate absolute elevation gain
    while ind < len(nodes) - 2:
        gain += abs(graph.nodes[nodes[ind]][ELEVATION_ATTR] - graph.nodes[nodes[ind+1]][ELEVATION_ATTR])
        ind += 1
    return gain

def geo_code(graph:nx.MultiDiGraph, nodes:list) -> list:
    geo_coded_nodes = list()

    # Convering node IDs to latitude and longitudes i.e geocoding them.
    for node in nodes:
        geo_coded_nodes.append([graph.nodes[node]['x'], graph.nodes[node]['y']])

    return geo_coded_nodes

def get_heuristic(elevation_gain_type:str, graph:nx.MultiDiGraph, attr:str) -> Callable:
    # A star always looks for lowest cost. If it is a min elevation gain, then each elevation added to length is costly and therefore remains positive.
    # If it is max elevation gain, for the heuristic we subtract it so that the higher elevations become lower cost so A star will look for it.
    multiplier = 1 if elevation_gain_type == "min" else -1
    return lambda x, y: (multiplier * (abs(graph.nodes[x][attr] - graph.nodes[y][attr])))



def algorithm(start_location:str, stop_location:str, route_type:str, elevation_gain_type:str, max_dist:int, API_KEY:str, to_geocode:bool) -> list:
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



    # Geocoding the start and stop locations to get their latitude and longitudes.
    geocode_start = ox.geocode(start_location)
    geocode_start_lat = geocode_start[0]
    geocode_start_lon = geocode_start[1]

    geocode_stop = ox.geocode(stop_location)
    geocode_stop_lat = geocode_stop[0]
    geocode_stop_lon = geocode_stop[1]

    # We generate the default region's graph, then generate the shortest route and using that we construct the final graph including the % increase from the shortest distance the user can set
    # as the furthest network distance to guarantee either that the user gets the route within some % of the shortest distance with either min/max, or just gets the shortest route.

    # Generating the default region's graph
    default_region_graph = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)

    # Finding the nearest nodes to the start and stop exact geocodes
    start_node = ox.nearest_nodes(G=default_region_graph, X=geocode_start_lon, Y=geocode_start_lat)
    stop_node = ox.nearest_nodes(G=default_region_graph, X=geocode_stop_lon, Y=geocode_stop_lat)

    # Generating the shortest path, calculating its distance and then adding on the user's settings
    shortest_path = ox.shortest_path(G=default_region_graph, orig=start_node, dest=stop_node, weight=LENGTH_ATTR, cpus=None)
    shortest_distance = nx.classes.function.path_weight(G=default_region_graph, path=shortest_path, weight=LENGTH_ATTR)
    shortest_distance_with_percentage_max_dist = shortest_distance * (1 + (float(max_dist)/100))

    # Generating the final graph, adding elevations via gmaps.
    graph = ox.graph.graph_from_address(address=start_location, dist=shortest_distance_with_percentage_max_dist, network_type=route_type, dist_type=DIST_TYPE)
    graph = ox.elevation.add_node_elevations_google(G=graph, api_key=API_KEY)

    # Finding the nearest nodes to the start and stop exact geocodes in the final graph
    start_node = ox.nearest_nodes(G=graph, X=geocode_start_lon, Y=geocode_start_lat)
    stop_node = ox.nearest_nodes(G=graph, X=geocode_stop_lon, Y=geocode_stop_lat)


    # A star algorithm, maintaining priority queue for cost to nodes
    pq = PriorityQueue()
    pq.put((0, start_node))
    came_from = {}
    cost_so_far = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    path_found = False

    # Getting heuristic function
    heuristic = get_heuristic(elevation_gain_type=elevation_gain_type, graph=graph, attr=ELEVATION_ATTR)


    while not pq.empty():
        current = pq.get()

        # Stored as tuple so getting Node ID and not priority
        current = current[1]

        if current == stop_node:
            path_found = True
            break
        # For all the edges of the current node
        for edge in graph.edges(current):
            from_node = edge[0]
            to_node = edge[1]
            # For all variations of that edge since it is a multigraph
            for edge_sub in graph[from_node][to_node].values():
                edge_weight = edge_sub.get(LENGTH_ATTR, None)
                new_cost = cost_so_far[current] + edge_weight
                if to_node not in cost_so_far or new_cost < cost_so_far[to_node]:
                    cost_so_far[to_node] = new_cost
                    # Cost with heuristic here as priority, and elevation difference as heuristic.
                    priority = new_cost + heuristic(current, to_node)
                    pq.put((priority, to_node))
                    came_from[to_node] = (current, edge_weight)

    # Getting the path back and calculating weight
    astar_path = []
    current = stop_node
    weight = 0
    while current != None:
        astar_path.append(current)
        if came_from[current] is not None:
            prev, length = came_from[current]
            weight += length
            current = prev
        else:
            current = came_from[current]

    astar_path.reverse()

    # If we did not find a path or if the path we found is too large, we return empty list
    if not path_found or weight > shortest_distance_with_percentage_max_dist:
        return []

    if to_geocode:
        return geo_code(graph=graph, nodes=astar_path)
    else:
        return astar_path
