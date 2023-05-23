from unittest import TestCase
import sys
sys.path.append('../../python')
import dijkstra
import osmnx as ox
import pytest

DEFAULT_REGION = "Amherst, MA"
KEY_LOCATION = "../../python/key.txt"

API_KEY = None
CICS_BUILDING_ADDRESS = "140 Governors Dr, Amherst, MA 01002"
DICKINSON_HALL_ADDRESS = "151 Orchard Hill Dr, Amherst, MA 01003"
MFA_BOSTON_ADDRESS = "465 Huntington Ave, Boston, MA 02115"

DRIVE_ROUTE_TYPE = "drive"
WALK_ROUTE_TYPE = "walk"
BIKE_ROUTE_TYPE = "bike"
MAX_DIST_DEFAULT = "15"

MIN_ELEVATION_GAIN = "minimize"
MAX_ELEVATION_GAIN = "maximize"

class TryTesting(TestCase):

    @pytest.fixture(autouse=True)
    def run_around_tests(arg):
        # Run before each test
        f = open(KEY_LOCATION)
        global API_KEY
        API_KEY = f.read()

        yield

        API_KEY = None

    def test_dijsktra_returns_path(self):
        start_address = CICS_BUILDING_ADDRESS
        stop_address = DICKINSON_HALL_ADDRESS
        route_type = DRIVE_ROUTE_TYPE
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = MAX_DIST_DEFAULT

        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost
        


    def test_dijkstra_drive_minimize(self):
        start_address = "21 Hallock St, Amherst, MA 01002"
        stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
        route_type = "drive"
        elevation_gain_type = MIN_ELEVATION_GAIN
        max_dist = "15"

        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost

    def test_dijkstra_walk_minimize(self):
        start_address = "21 Hallock St, Amherst, MA 01002"
        stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
        route_type = "walk"
        elevation_gain_type = MIN_ELEVATION_GAIN
        max_dist = "15"

        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost

    def test_dijkstra_bike_minimize(self):
        start_address = "21 Hallock St, Amherst, MA 01002"
        stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
        route_type = "bike"
        elevation_gain_type = MIN_ELEVATION_GAIN
        max_dist = "15"
        
        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost
    
    def test_dijkstra_drive_maximize(self):
        start_address = "21 Hallock St, Amherst, MA 01002"
        stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
        route_type = "drive"
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = "15"
        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost
    
    # This test case takes too much time to run so commenting this out
    # def test_dijkstra_walk_maximize(self):
    #     start_address = "21 Hallock St, Amherst, MA 01002"
    #     stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
    #     route_type = "walk"
    #     elevation_gain_type = MAX_ELEVATION_GAIN
    #     max_dist = "15"

    #     G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
    #     G = ox.elevation.add_node_elevations_google(G, API_KEY)

    #     geocode_start = ox.geocode(start_address)
    #     geocode_start_lat = geocode_start[0]
    #     geocode_start_lon = geocode_start[1]

    #     geocode_stop = ox.geocode(stop_address)
    #     geocode_stop_lat = geocode_stop[0]
    #     geocode_stop_lon = geocode_stop[1]

    #     start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
    #     destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

    #     default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
    #     default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
    #     dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
    #     dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
    #     assert len(dijkstra_path) != 0, "the list is not empty"

    #     "The cost of the path should be less than or equal to the default one."
    #     assert dijkstra_path_cost <= default_shortest_path_cost
    
    
    def test_dijkstra_bike_maximize(self):
        start_address = "21 Hallock St, Amherst, MA 01002"
        stop_address = "151 Orchard Hill Dr, Amherst, MA 01003"
        route_type = "bike"
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = "15"
        G = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        G = ox.elevation.add_node_elevations_google(G, API_KEY)

        geocode_start = ox.geocode(start_address)
        geocode_start_lat = geocode_start[0]
        geocode_start_lon = geocode_start[1]

        geocode_stop = ox.geocode(stop_address)
        geocode_stop_lat = geocode_stop[0]
        geocode_stop_lon = geocode_stop[1]

        start = ox.nearest_nodes(G, geocode_start_lon, geocode_start_lat)
        destination = ox.nearest_nodes(G, geocode_stop_lon, geocode_stop_lat)

        default_shortest_path_by_distance = dijkstra.get_shortest_length_path(G, start, destination)
        default_shortest_path_cost = dijkstra.calculate_path_length(G, default_shortest_path_by_distance)
        dijkstra_path = dijkstra.algorithm(start_address, stop_address, route_type, elevation_gain_type, max_dist, API_KEY, to_geocode=False)
        dijkstra_path_cost = dijkstra.calculate_path_length(G, dijkstra_path)
        
        assert len(dijkstra_path) != 0, "the list is not empty"

        "The cost of the path should be less than or equal to the default one."
        assert dijkstra_path_cost <= default_shortest_path_cost