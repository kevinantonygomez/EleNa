from unittest import TestCase
import a_star
import pytest
import osmnx as ox
import networkx as nx

# global API Key
API_KEY = None
KEY_LOCATION = "python/key.txt"

# Address constants
CICS_BUILDING_ADDRESS = "140 Governors Dr, Amherst, MA 01002"
CICS_DRIVE_NODE_ID = 66690339
CICS_WALK_NODE_ID = 3169719090
CICS_BIKE_NODE_ID = 66627276
DICKINSON_HALL_ADDRESS = "151 Orchard Hill Dr, Amherst, MA 01003"
DICKINSON_HALL_DRIVE_NODE_ID = 66648487
DICKINSON_HALL_WALK_NODE_ID = 8412485620
DICKINSON_HALL_BIKE_NODE_ID = 8412485620
MFA_BOSTON_ADDRESS = "465 Huntington Ave, Boston, MA 02115"

# Default region(restricted to Amherst)
DEFAULT_REGION = "Amherst, MA"

# Fixed constants for graph construction
DRIVE_ROUTE_TYPE = "drive"
WALK_ROUTE_TYPE = "walk"
BIKE_ROUTE_TYPE = "bike"
MAX_DIST_DEFAULT = "15"
MIN_ELEVATION_GAIN = "min"
MAX_ELEVATION_GAIN = "max"


class TryTesting(TestCase):

    @pytest.fixture(autouse=True)
    def run_around_tests(arg):
        # Run before each test
        f = open(KEY_LOCATION)
        global API_KEY
        API_KEY = f.read()

        yield

        API_KEY = None

    def test_astar_returns_empty_list_if_invalid_location(self):
        # Since the stop address is outside of amherst, we expect empty list as that is outside the defined region.

        # Inside Amherst
        start_address = CICS_BUILDING_ADDRESS
        # Outside Amherst
        stop_address = MFA_BOSTON_ADDRESS
        route_type = DRIVE_ROUTE_TYPE
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = MAX_DIST_DEFAULT
        our_astar_path = a_star.algorithm(start_location=start_address, stop_location=stop_address, route_type=route_type, elevation_gain_type=elevation_gain_type, max_dist=max_dist, API_KEY=API_KEY, to_geocode=False)

        assert len(our_astar_path) == 0, "With an invalid stop address outside of the defined region, the output path should be an empty list"


    def test_astar_drive(self):
        start_address = CICS_BUILDING_ADDRESS
        stop_address = DICKINSON_HALL_ADDRESS
        route_type = DRIVE_ROUTE_TYPE
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = MAX_DIST_DEFAULT

        
        default_region_graph = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        default_region_graph = ox.elevation.add_node_elevations_google(G=default_region_graph, api_key=API_KEY)

        our_astar_path = a_star.algorithm(start_location=start_address, stop_location=stop_address, route_type=route_type, elevation_gain_type=elevation_gain_type, max_dist=max_dist, API_KEY=API_KEY, to_geocode=False)
        our_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=our_astar_path, weight=a_star.LENGTH_ATTR)
        our_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=our_astar_path)

        
        heuristic = a_star.get_heuristic(elevation_gain_type=elevation_gain_type, graph=default_region_graph, attr=a_star.ELEVATION_ATTR)
        networkx_astar_path = nx.astar_path(G=default_region_graph, source=CICS_DRIVE_NODE_ID, target=DICKINSON_HALL_DRIVE_NODE_ID, heuristic=heuristic, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=networkx_astar_path, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=networkx_astar_path)

        assert len(our_astar_path) != 0, "With two valid addresses, the output should be a non empty path."

        assert our_astar_path[0] == networkx_astar_path[0] == CICS_DRIVE_NODE_ID, "The start node is not the right one" 
        assert our_astar_path[-1] == networkx_astar_path[-1] == DICKINSON_HALL_DRIVE_NODE_ID, "The stop node is not the right one"

        assert our_astar_path_cost <= networkx_astar_path_cost, "The cost of the path should be less than or equal to the default one."
        assert our_astar_path_gain >= networkx_astar_path_gain, "The elevation of the path should be greater than or equal to the default one."

    def test_astar_walk(self):
        start_address = CICS_BUILDING_ADDRESS
        stop_address = DICKINSON_HALL_ADDRESS
        route_type = WALK_ROUTE_TYPE
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = MAX_DIST_DEFAULT

        default_region_graph = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        default_region_graph = ox.elevation.add_node_elevations_google(G=default_region_graph, api_key=API_KEY)

        our_astar_path = a_star.algorithm(start_location=start_address, stop_location=stop_address, route_type=route_type, elevation_gain_type=elevation_gain_type, max_dist=max_dist, API_KEY=API_KEY, to_geocode=False)
        our_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=our_astar_path, weight=a_star.LENGTH_ATTR)
        our_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=our_astar_path)

        
        heuristic = a_star.get_heuristic(elevation_gain_type=elevation_gain_type, graph=default_region_graph, attr=a_star.ELEVATION_ATTR)
        networkx_astar_path = nx.astar_path(G=default_region_graph, source=CICS_WALK_NODE_ID, target=DICKINSON_HALL_WALK_NODE_ID, heuristic=heuristic, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=networkx_astar_path, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=networkx_astar_path)

        assert len(our_astar_path) != 0, "With two valid addresses, the output should be a non empty path."

        assert our_astar_path[0] == networkx_astar_path[0] == CICS_WALK_NODE_ID, "The start node is not the right one" 
        assert our_astar_path[-1] == networkx_astar_path[-1] == DICKINSON_HALL_WALK_NODE_ID, "The stop node is not the right one"

        assert our_astar_path_cost <= networkx_astar_path_cost, "The cost of the path should be less than or equal to the default one."
        assert our_astar_path_gain >= networkx_astar_path_gain, "The elevation of the path should be greater than or equal to the default one."

    def test_astar_bike(self):
        start_address = CICS_BUILDING_ADDRESS
        stop_address = DICKINSON_HALL_ADDRESS
        route_type = BIKE_ROUTE_TYPE
        elevation_gain_type = MAX_ELEVATION_GAIN
        max_dist = MAX_DIST_DEFAULT

        default_region_graph = ox.graph_from_place(query=DEFAULT_REGION, network_type=route_type)
        default_region_graph = ox.elevation.add_node_elevations_google(G=default_region_graph, api_key=API_KEY)

        our_astar_path = a_star.algorithm(start_location=start_address, stop_location=stop_address, route_type=route_type, elevation_gain_type=elevation_gain_type, max_dist=max_dist, API_KEY=API_KEY, to_geocode=False)
        our_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=our_astar_path, weight=a_star.LENGTH_ATTR)
        our_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=our_astar_path)

        
        heuristic = a_star.get_heuristic(elevation_gain_type=elevation_gain_type, graph=default_region_graph, attr=a_star.ELEVATION_ATTR)
        networkx_astar_path = nx.astar_path(G=default_region_graph, source=CICS_BIKE_NODE_ID, target=DICKINSON_HALL_BIKE_NODE_ID, heuristic=heuristic, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_cost = nx.classes.function.path_weight(G=default_region_graph, path=networkx_astar_path, weight=a_star.LENGTH_ATTR)
        networkx_astar_path_gain = a_star.calculate_elevation_gain(graph=default_region_graph, nodes=networkx_astar_path)

        assert len(our_astar_path) != 0, "With two valid addresses, the output should be a non empty path."

        assert our_astar_path[0] == networkx_astar_path[0] == CICS_BIKE_NODE_ID, "The start node is not the right one" 
        assert our_astar_path[-1] == networkx_astar_path[-1] == DICKINSON_HALL_BIKE_NODE_ID, "The stop node is not the right one"

        assert our_astar_path_cost <= networkx_astar_path_cost, "The cost of the path should be less than or equal to the default one."
        assert our_astar_path_gain >= networkx_astar_path_gain, "The elevation of the path should be greater than or equal to the default one."
