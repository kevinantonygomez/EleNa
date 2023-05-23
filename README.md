# EleNa
CS 520 Final Project\
Semester: Spring 2023\
Team: 3 Grads\
Members: Kevin Antony Gomez, Armand Asnani, Maneesha Tejani

## What is EleNa?
EleNA is a configurable web-based navigation app that provides users with the best route from point A to point B based on whether they want to maximize or minimize their elevation gain during the journey.
Users can also state how much further they are willing to travel in addition to the shortest distance to find the route that not only helps them achieve their elevation requirements but also gets them to their destination without adding too much distance.\
**Note:** This system is currently configured to only work within Amherst.

## Requirements

### API:
1. For the embedded map, sign up and get an API key from: https://developers.arcgis.com.
2. Set const apiKey = "Your_API_Key" in indexScript.js.
3. For the elevation data, sign up and get an API key for Elevation: https://developers.google.com/maps
4. Create a file called "key.txt" in the 'python' folder and paste the API key. Ensure no newlines and that only the API key is included (in the first line)

### Packages, Modules and Dependencies:

**Web:**
1. Node.js: Download the latest version (https://nodejs.org/en). Must be >= v.16.
2. NPM: Set up the npm command line interface (https://www.npmjs.com/).
3. Express.js: npm i express (https://www.npmjs.com/package/express)
4. JSDOM: npm i jsdom (https://www.npmjs.com/package/jsdom)
5. jQuery: npm i jquery (https://www.npmjs.com/package/jquery)
6. Jest: npm install --save-dev jest (https://jestjs.io/docs/getting-started)

**Python:**
1. NetworkX: pip install networkx (https://networkx.org/)
2. OSMnx: pip install osmnx (https://geoffboeing.com/publications/osmnx-complex-street-networks/)
3. Flask: pip install flask (https://flask.palletsprojects.com/en/2.3.x/)
4. Matplotlib: pip install matplotlib (https://matplotlib.org/)
5. Pytest: pip install pytest (https://docs.pytest.org/en/7.1.x/getting-started.html)

## Setup/Execution

1. Once the requirements are met, to start the python backend/flask app, run 'python elena.py' in the 'python' folder. This will run the app on port 2000.
2. To run the server, run 'node server.js' in the root directory. This will run the webpage on port 3000.
3. After this, go to: http://127.0.0.1:3000/ and the webpage should be live and running!
