# Event-detection-in-real-time-data-
Processing time-evolving social networks in order to detect anomaly instants, namely moments when the network behavior deviates from the remaining by using a sliding window decomposition with statistical tools.

## File Structure & running
Contains 2 .py files 
basic.py, method.py
- Output events.csv, nodes.csv, final_evaluation.csv.

From basic.py and for every window W of length L we call the method.py sending the values:
- Factors, which is the number of fuctor in tensor decomposition.
- l_size, which is the Length of every Window in timestamps.
- stations, which is the number of stations, participating in our network.
- a, which is the decomposed list of the current window W
- y, the number of the repetion we are currently executing.

## Input Data format

In basic.py, we import our data which are bike trips between stations in Washington, D.C.
Then we have to format this data to a list in order to decompose them. For this purpose, we format our data (section table in basic.py) in an 3D Adjacency matrix where the list correspond to (Time x Nodes x Nodes):
 - Time (the hour the trip took place)
 - Nodes (the starting station)
 - Nodes (the ending station)
 
 \line
 After we call method.py
 
