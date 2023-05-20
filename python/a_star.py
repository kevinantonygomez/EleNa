
import osmnx as ox
import networkx as nx
from queue import PriorityQueue
def algorithm(start_location:str, stop_location:str, route_type:str, elevation_gain_type:str, max_dist:str):
    # call required methods here.

    multiplier = 1 if elevation_gain_type == "min" else -1

    geocode_start = ox.geocode(start_location)
    geocode_start_lat = geocode_start[0]
    geocode_start_lon = geocode_start[1]
    geocode_stop = ox.geocode(stop_location)
    geocode_stop_lat = geocode_stop[0]
    geocode_stop_lon = geocode_stop[1]

    # print("geocode_start: ", geocode_start)
    # print("geocode_stop: ", geocode_stop)

    amherst_graph = ox.graph_from_place(query="Amherst, MA", network_type=route_type)

    start_node = ox.nearest_nodes(amherst_graph, geocode_start_lon, geocode_start_lat)
    stop_node = ox.nearest_nodes(amherst_graph, geocode_stop_lon, geocode_stop_lat)

    print("start: ", start_node)
    print("stop: ", stop_node)

    shortest_path = ox.shortest_path(amherst_graph, start_node, stop_node, weight="length", cpus=None)
    shortest_distance = nx.classes.function.path_weight(amherst_graph, shortest_path, weight="length")

    graph = ox.graph.graph_from_address(address=start_location, dist=(shortest_distance * (1 + (int(max_dist)/100))), network_type="drive", dist_type="network")
    graph = ox.elevation.add_node_elevations_google(graph, "API_KEY")

    pq = PriorityQueue()
    pq.put(start_node, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    while not pq.empty():
        current = pq.get()

        if current == stop_node:
            break

        for edge in graph.edges(current):
            from_node = edge[0]
            to_node = edge[1]
            for edge_sub in graph[from_node][to_node].values():                   
                new_cost = cost_so_far[current] + edge_sub.get('length', None)
                if to_node not in cost_so_far or new_cost < cost_so_far[to_node]:
                    cost_so_far[to_node] = new_cost
                    priority = new_cost + (multiplier * (abs(graph.nodes[current]['elevation'] - graph.nodes[to_node]['elevation'])))
                    pq.put(to_node, priority)
                    came_from[to_node] = current

        
    cost = 0
    my_path = []
    current = stop_node
    while current != None:
        my_path.append(current)
        current = came_from[current]

    my_path.reverse()


    print("my path: ", my_path)
    print("my cost: ", cost_so_far[stop_node])
    print("my path length: ", len(my_path))


    path = nx.astar_path(graph, start_node, stop_node, lambda node,target: (multiplier * (abs(graph.nodes[node]['elevation'] - graph.nodes[target]['elevation']))), weight="length")
    cost = nx.classes.function.path_weight(graph, path, weight="length")

    print("astar path: ", path)
    print("astar cost: ", cost)
    print("astar path length: ", len(path))
    return my_path
