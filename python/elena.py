import osmnx as ox
from osmnx import distance as oxd
import matplotlib.pyplot as plt
import random
import networkx as nx
from osmnx import elevation
from osmnx.distance import shortest_path
import folium
import requests
import json
from django.http import JsonResponse
from flask import Flask, request, jsonify
from flask_cors import CORS


def get_geocodes(nodes_list:list, G:nx.classes.multidigraph.MultiDiGraph):
    geocodes_dict = dict()
    for node in nodes_list:
        geocodes_dict[node] = (G.nodes[node]['y'], G.nodes[node]['x'])
    # [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path_nodes_ids]
    return geocodes_dict


def get_all_elevations(nodes_list:list, G:nx.classes.multidigraph.MultiDiGraph):
    elevations_dict = dict()
    geocodes_dict = get_geocodes(nodes_list, G)

    for key in geocodes_dict.keys():
        lat = geocodes_dict[key][0]
        long = geocodes_dict[key][1]
        url = f"https://api.opentopodata.org/v1/aster30m?locations={lat},{long}"
        response = requests.request("GET", url)
        json_response = json.loads(response.text)
        if json_response['status'] == 'OK' and len(json_response['results']) > 0:
            elevations_dict[key] = json_response['results'][0]['elevation'] # in meters
            print(f"Lat:{lat}, Long:{long}, Elevation:{elevations_dict[key]}")
    return elevations_dict


def get_elevation(lat_long:tuple):
    url = f"https://api.opentopodata.org/v1/aster30m?locations={lat_long[0]},{lat_long[1]}"
    response = requests.request("GET", url)
    json_response = json.loads(response.text)
    if json_response['status'] == 'OK' and len(json_response['results']) > 0:
        return json_response['results'][0]['elevation'] # in meters
    return None



app = Flask(__name__)
CORS(app)
@app.route('/get_route', methods=['POST'])
def handle_request():
    data = request.get_json()
    start_location = data["startLocation"]
    stop_location = data["stopLocation"]
    route_type = data["routeType"]
    elevation_gain_type = data["elevationGainType"]
    max_dist = data["maxDist"]

    # Do something with the data

    # Return the result to the client
    result = "result_here"
    response = jsonify({'result': result})
    return response

if __name__ == '__main__':
    app.run(port = 5000)
