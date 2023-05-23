import osmnx as ox
from flask import Flask, request, jsonify
from flask_cors import CORS
import dijkstra as dijkstra
import a_star as a_star
import json

KEY = None

def check_addresses(start_location:str, stop_location:str):
    try:
        start_location_split = start_location.split(",")
        if len(start_location_split) >= 6: start_location_split.pop(0)
        start_location = ",".join(start_location_split)
        start_geocode = ox.geocode(start_location)
        print("start_location: ", start_geocode)
    except:
        print("No geocode for start_location")
        return "invalid_start"
    try:
        stop_location_split = stop_location.split(",")
        if len(stop_location_split) >= 6: stop_location_split.pop(0)
        stop_location = ",".join(stop_location_split)
        stop_geocode = ox.geocode(stop_location)
        print("stop_location: ", stop_geocode)
    except:
        print("No geocode for stop_location")
        return "invalid_stop"
    return (start_location, stop_location)



def main(start_location:str, stop_location:str, route_type:str, elevation_gain_type:str, max_dist:str, algorithm:str):
    check_res = check_addresses(start_location, stop_location)
    if type(check_res) != tuple:
        return check_res

    start_location = check_res[0]
    stop_location = check_res[1]

    if algorithm == "dijkstra":
        gen_route = dijkstra.algorithm(start_location, stop_location, route_type, elevation_gain_type, max_dist, KEY, to_geocode=True)
    elif algorithm == "A*":
        gen_route = a_star.algorithm(start_location=start_location, stop_location=stop_location, route_type=route_type, elevation_gain_type=elevation_gain_type, max_dist=max_dist, API_KEY=KEY, to_geocode=True)

    return gen_route



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
    algorithm = data["algorithm"]

    res = main(start_location, stop_location, route_type, elevation_gain_type, max_dist, algorithm)
    # Return the result to the client
    if res == None:
        response = jsonify({'error': "error"}), 400
    elif res == []:
        response = jsonify({'error': "no_path_found"}), 400
    elif res == "invalid_start" or res == "invalid_stop":
        response = jsonify({'error': res}), 400
    else:
        response = json.dumps(res), 200
    return response


if __name__ == '__main__':
    f = open("key.txt")
    KEY = f.read()
    app.run(port = 2000, debug=True)
