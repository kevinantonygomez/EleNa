# EleNa
CS 520 Final Project\
Semester: Spring 2023\
Team: 3 Grads\
Members: Kevin Antony Gomez, Armand Asnani, Maneesha Tejani

## Requirements

### API:
1. Sign up and get an API key from: https://developers.arcgis.com.
2. Set const apiKey = "Your_API_Key" in indexScript.js.

### Packages, Modules and Dependencies:

**Web:**
1. Node.js: Download the latest version (https://nodejs.org/en). Must be >= v.16.
2. NPM: Set up the npm command line interface (https://www.npmjs.com/).
3. Express.js: npm i express (https://www.npmjs.com/package/express)
4. JSDOM: npm i jsdom (https://www.npmjs.com/package/jsdom)
5. jQuery: npm i jquery (https://www.npmjs.com/package/jquery)

**Python:**
1. NetworkX: pip install networkx (https://networkx.org/)
2. OSMnx: pip install osmnx (https://geoffboeing.com/publications/osmnx-complex-street-networks/)
3. Flask: pip install flask (https://flask.palletsprojects.com/en/2.3.x/)
4. Matplotlib: pip install matplotlib (https://matplotlib.org/)

**Opentopodata:**
1. To host elevation data locally using opentopodata (https://www.opentopodata.org/#host-your-own), first install docker (https://docs.docker.com/get-docker/)
2. Now, at the same level as public_html and python, git clone https://github.com/ajnisbet/opentopodata.git
3. cd opentopodata
4. Add config.yaml from opentopodata_dataset
5. cd data
6. Add aster30m folder from opentopodata_dataset
7. make build
8. make run
9. Ensure server starts on http://localhost:5000/
10. Make API calls as such: http://localhost:5000/v1/aster30m?locations={lat},{long}
